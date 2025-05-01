from fastapi import APIRouter, File, UploadFile, HTTPException, Request
from ..models.ml_model import get_prediction
import io
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/predict")
async def predict(request: Request, file: UploadFile = File(...)):
    """
    Endpoint to predict the class of an uploaded image
    """
    try:
        logger.info(f"Received prediction request for file: {file.filename}")
        
        # Check if the file is an image
        if not file.content_type.startswith("image/"):
            error_msg = f"File must be an image, got {file.content_type}"
            logger.warning(error_msg)
            raise HTTPException(status_code=400, detail=error_msg)
        
        # Read the file
        try:
            image_bytes = await file.read()
            logger.info(f"Successfully read {len(image_bytes)} bytes from file")
            
            if len(image_bytes) == 0:
                raise HTTPException(status_code=400, detail="Empty file uploaded")
                
        except Exception as e:
            error_msg = f"Error reading file: {str(e)}"
            logger.error(error_msg)
            raise HTTPException(status_code=400, detail=error_msg)
        
        try:
            # Get prediction
            logger.info("Calling prediction model...")
            predictions = get_prediction(image_bytes)
            logger.info("Prediction successful")
            
            return {
                "filename": file.filename,
                "content_type": file.content_type,
                "predictions": predictions
            }
        except Exception as e:
            error_msg = f"Error during prediction: {str(e)}"
            logger.error(error_msg)
            raise HTTPException(status_code=500, detail=error_msg)
            
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)