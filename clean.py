import pathlib 
import shutil

home_dir = pathlib.Path.home()
dataset_dir = home_dir / ".cache" / "huggingface" / "datasets"
    
shutil.rmtree(str(dataset_dir))
