import React, { useState } from "react";
import { Container, Card } from "react-bootstrap";
import ImageUpload from "../components/ImageUpload";
import PredictionResult from "../components/PredictionResult";

const Home = () => {
  const [predictionResult, setPredictionResult] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);

  const handlePredictionResult = (result, preview) => {
    setPredictionResult(result);
    setImagePreview(preview);
  };

  return (
    <Container className="py-4">
      <Card className="shadow-sm" style={{ marginTop: "100px" }}>
        <Card.Body>
          <h1 className="text-center mb-4">Image Classification App</h1>
          <p className="lead text-center">
            Upload an image to identify what's in it using our machine learning
            model.
          </p>

          <ImageUpload onPredictionResult={handlePredictionResult} />

          {predictionResult && (
            <PredictionResult
              result={predictionResult}
              imagePreview={imagePreview}
            />
          )}
        </Card.Body>
      </Card>
    </Container>
  )
};

export default Home;