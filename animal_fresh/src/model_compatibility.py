# model_compatibility.py
"""
Compatibility layer for handling model version mismatches.
Fixes scikit-learn and XGBoost compatibility issues.
"""

import joblib
import numpy as np
import pandas as pd
import warnings
import sklearn
import os

# --- NUCLEAR COMPATIBILITY PATCHES ---
# These run on import to ensure all scikit-learn components are fixed globally

def apply_global_patches():
    """Apply global monkey-patches to scikit-learn classes."""
    try:
        # Patch both the top-level alias and the internal class
        targets = []
        try:
            from sklearn.impute import SimpleImputer
            targets.append(SimpleImputer)
        except ImportError:
            pass
            
        try:
            from sklearn.impute._base import SimpleImputer as BaseSimpleImputer
            if BaseSimpleImputer not in targets:
                targets.append(BaseSimpleImputer)
        except ImportError:
            pass
        
        import numpy as np
        
        for ImputerClass in targets:
            # Patch 1: SimpleImputer._fill_dtype property
            # Use a robust getter that cannot fail
            if not hasattr(ImputerClass, '_fill_dtype_patched_prop'):
                def get_fill_dtype(self):
                    try:
                        # Data descriptor precedence means we must explicitly check dict
                        if hasattr(self, '__dict__') and '_fill_dtype' in self.__dict__:
                            return self.__dict__['_fill_dtype']
                        
                        # Fallback to _fit_dtype
                        if hasattr(self, '_fit_dtype'):
                            return self._fit_dtype
                            
                        # Fallback to statistics dtype
                        if hasattr(self, 'statistics_') and self.statistics_ is not None:
                            if hasattr(self.statistics_, 'dtype'):
                                return self.statistics_.dtype
                                
                        return np.dtype('float64')
                    except Exception as e:
                        print(f"Warning: Safe property getter failed: {e}")
                        return np.dtype('float64')
                    
                def set_fill_dtype(self, value):
                    try:
                        if hasattr(self, '__dict__'):
                            self.__dict__['_fill_dtype'] = value
                    except:
                        pass
                    
                # Overwrite the class attribute with our managed property
                ImputerClass._fill_dtype = property(get_fill_dtype, set_fill_dtype)
                ImputerClass._fill_dtype_patched_prop = True
                print(f"Applied property patch to {ImputerClass}")
                
            # Patch 1.5: Also patch transform method as a second layer of defense
            if not hasattr(ImputerClass, '_transform_patched'):
                original_transform = ImputerClass.transform
                
                def robust_transform(self, X, *args, **kwargs):
                    # Ensure _fill_dtype exists before passing to original
                    if not hasattr(self, '_fill_dtype') or self._fill_dtype is None:
                        # This should trigger our setter (which sets dict) or be handled by property
                        try:
                            self._fill_dtype = getattr(self, '_fit_dtype', np.dtype('float64'))
                        except:
                            pass
                    
                    try:
                        return original_transform(self, X, *args, **kwargs)
                    except AttributeError as e:
                        if "_fill_dtype" in str(e):
                             # Last resort: Force inject into __dict__ blindly
                             if hasattr(self, '__dict__'):
                                 self.__dict__['_fill_dtype'] = np.dtype('float64')
                             return original_transform(self, X, *args, **kwargs)
                        raise
                        
                ImputerClass.transform = robust_transform
                ImputerClass._transform_patched = True
                print(f"Applied method patch to {ImputerClass}")

        # Patch 2: ColumnTransformer.n_jobs forced to 1
        from sklearn.compose import ColumnTransformer
        import functools
        
        # Patch the __init__ for new objects
        if not hasattr(ColumnTransformer, '_init_patched'):
            original_init = ColumnTransformer.__init__
            @functools.wraps(original_init)
            def patched_init(self, *args, **kwargs):
                if 'n_jobs' in kwargs:
                    kwargs['n_jobs'] = 1
                original_init(self, *args, **kwargs)
                self.n_jobs = 1
            ColumnTransformer.__init__ = patched_init
            ColumnTransformer._init_patched = True
        
        # Patch the transform for existing objects
        if not hasattr(ColumnTransformer, '_transform_patched'):
            original_ct_transform = ColumnTransformer.transform
            def patched_ct_transform(self, X, **kwargs):
                # FORCE sequential consistency
                if hasattr(self, 'n_jobs'):
                    self.n_jobs = 1
                return original_ct_transform(self, X, **kwargs)
            ColumnTransformer.transform = patched_ct_transform
            ColumnTransformer._transform_patched = True

        print("Global patches applied successfully")

    except Exception as e:
        print(f"Warning: Failed to apply some global patches: {e}")

# Apply patches immediately on module load
apply_global_patches()

def patch_simpleimputer():
    """Redundant stub for backward compatibility."""
    apply_global_patches()

def patch_xgboost_classifier():
    """Monkey-patch XGBClassifier and XGBModel to handle deprecated parameters."""
    try:
        from xgboost import XGBClassifier, XGBModel
        
        def create_patched_get_params(original_class, class_name):
            original_get_params = original_class.get_params
            
            def patched_get_params(self, deep=True):
                try:
                    return original_get_params(self, deep)
                except AttributeError as e:
                    error_msg = str(e)
                    deprecated_params = ['use_label_encoder', 'gpu_id', 'gpu_predictor', 
                                     'predictor', 'updater', 'n_gpus', 'process_type',
                                     'grow_policy', 'max_leaves', 'max_bin', 'scale_pos_weight']
                    
                    temp_attrs = {}
                    missing_attr = None
                    if "has no attribute" in error_msg:
                        try:
                            missing_attr = error_msg.split("has no attribute '")[1].split("'")[0]
                            if missing_attr not in deprecated_params:
                                deprecated_params.append(missing_attr)
                        except:
                            pass
                    
                    for param in deprecated_params:
                        if (missing_attr and param == missing_attr) or (param in error_msg and not hasattr(self, param)):
                            temp_attrs[param] = None
                            setattr(self, param, None)
                    
                    try:
                        params = original_get_params(self, deep)
                        for param in deprecated_params:
                            if param in params:
                                del params[param]
                        return params
                    finally:
                        for param, value in temp_attrs.items():
                            if value is None and hasattr(self, param):
                                delattr(self, param)
            
            original_class.get_params = patched_get_params
        
        def create_patched_predict(original_class):
            original_predict = original_class.predict
            
            def patched_predict(self, X, **kwargs):
                try:
                    return original_predict(self, X, **kwargs)
                except AttributeError as e:
                    error_msg = str(e)
                    missing_attrs = ['predictor', 'use_label_encoder', 'gpu_id']
                    temp_attrs = {}
                    
                    for attr in missing_attrs:
                        if attr in error_msg and not hasattr(self, attr):
                            temp_attrs[attr] = None
                            setattr(self, attr, None)
                    
                    try:
                        return original_predict(self, X, **kwargs)
                    finally:
                        for attr, value in temp_attrs.items():
                            if value is None and hasattr(self, attr):
                                delattr(self, attr)
            
            original_class.predict = patched_predict
        
        create_patched_get_params(XGBClassifier, "XGBClassifier")
        create_patched_get_params(XGBModel, "XGBModel")
        create_patched_predict(XGBClassifier)
        create_patched_predict(XGBModel)
        
    except Exception as e:
        print(f"Failed to patch XGBoost classes: {e}")

def fix_simpleimputer_compatibility(pipeline):
    """
    Instance-level fix as a second layer of defense.
    """
    from sklearn.impute import SimpleImputer
    from sklearn.pipeline import Pipeline
    from sklearn.compose import ColumnTransformer

    processed_ids = set()

    def walk_and_fix(obj, depth=0):
        if depth > 20 or obj is None or id(obj) in processed_ids:
            return
        processed_ids.add(id(obj))

        # Force sequential
        if hasattr(obj, 'n_jobs'):
            try: obj.n_jobs = 1
            except: pass

        if isinstance(obj, Pipeline):
            if hasattr(obj, 'steps'):
                for _, step in obj.steps:
                    walk_and_fix(step, depth + 1)
        elif isinstance(obj, ColumnTransformer):
            if hasattr(obj, 'transformers'):
                for _, t, _ in obj.transformers:
                    walk_and_fix(t, depth + 1)
            if hasattr(obj, 'transformers_'):
                for _, t, _ in obj.transformers_:
                    walk_and_fix(t, depth + 1)
        elif isinstance(obj, SimpleImputer):
            if not hasattr(obj, '_fill_dtype'):
                val = getattr(obj, '_fit_dtype', None)
                if val is None and hasattr(obj, 'statistics_') and obj.statistics_ is not None:
                    try: val = obj.statistics_.dtype
                    except: pass
                obj._fill_dtype = val or np.dtype('float64')
        elif isinstance(obj, (list, tuple)):
            for item in obj:
                walk_and_fix(item, depth + 1)
        elif isinstance(obj, dict):
            for item in obj.values():
                walk_and_fix(item, depth + 1)
        elif hasattr(obj, '__dict__'):
            for attr_name in list(obj.__dict__.keys()):
                try:
                    attr_value = getattr(obj, attr_name)
                    if attr_value is not None and not isinstance(attr_value, (int, float, str, bool, np.ndarray, pd.DataFrame)):
                        walk_and_fix(attr_value, depth + 1)
                except: pass
    
    walk_and_fix(pipeline)
    return pipeline

def fix_xgboost_compatibility(model):
    """Save and reload booster to fix binary compatibility."""
    try:
        if hasattr(model, 'get_booster'):
            import tempfile
            import os
            if hasattr(model, 'use_label_encoder'):
                delattr(model, 'use_label_encoder')
            
            with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as tmp:
                temp_path = tmp.name
            try:
                booster = model.get_booster()
                booster.save_model(temp_path)
                booster.load_model(temp_path)
            finally:
                if os.path.exists(temp_path): os.unlink(temp_path)
    except: pass
    return model

def load_compatible_models():
    """Load models with all layers of compatibility fixes."""
    try:
        # 1. Apply global class-level patches
        apply_global_patches()
        patch_xgboost_classifier()
        
        # 2. Determine models directory
        models_dir = "models"
        if not os.path.exists(models_dir):
            models_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "models")
        models_dir = os.path.normpath(models_dir)
        
        # 3. Load files
        stage1_pipeline = joblib.load(os.path.join(models_dir, "stage1_pipeline.pkl"))
        stage2_models = joblib.load(os.path.join(models_dir, "stage2_models.pkl"))
        category_encoder = joblib.load(os.path.join(models_dir, "category_encoder.pkl"))
        disease_encoders = joblib.load(os.path.join(models_dir, "disease_encoders.pkl"))
        
        # 4. Instance-level fixes (Layer 2)
        stage1_pipeline = fix_simpleimputer_compatibility(stage1_pipeline)
        for cat, pipe in stage2_models.items():
            stage2_models[cat] = fix_simpleimputer_compatibility(pipe)
        
        # 5. XGBoost specific fixes (Layer 3)
        m1 = stage1_pipeline.named_steps.get("model")
        if m1: stage1_pipeline.named_steps["model"] = fix_xgboost_compatibility(m1)
        for cat, pipe in stage2_models.items():
            m2 = pipe.named_steps.get("model")
            if m2: pipe.named_steps["model"] = fix_xgboost_compatibility(m2)
            
        return stage1_pipeline, stage2_models, category_encoder, disease_encoders
    except Exception as e:
        print(f"Critical error loading models: {e}")
        raise

def suppress_sklearn_warnings():
    """Suppress sklearn version mismatch warnings."""
    warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")
    warnings.filterwarnings("ignore", category=FutureWarning, module="sklearn")
    warnings.filterwarnings("ignore", message="Trying to unpickle estimator")
