import React from "react";
import { Card, ProgressBar } from "react-bootstrap";

const PredictionResult = ({ result, imagePreview }) => {
  if (!result) return null;

  return (
    <Card className="my-4">
      <Card.Header as="h5">Classification Results</Card.Header>
      <Card.Body>
        <div className="row">
          <div className="col-md-6">
            <img
              src={imagePreview}
              alt="Uploaded"
              style={{ maxWidth: "100%", maxHeight: "300px" }}
              className="img-thumbnail"
            />
            <p className="mt-2">
              <strong>Filename:</strong> {result.filename}
            </p>
          </div>
          <div className="col-md-6">
            <h5>Top 5 Predictions:</h5>
            {result.predictions.map((prediction, index) => (
              <div key={index} className="mb-3">
                <div className="d-flex justify-content-between mb-1">
                  <span>{prediction.class}</span>
                  <span>{(prediction.probability * 100).toFixed(2)}%</span>
                </div>
                <ProgressBar
                  variant={index === 0 ? "success" : "info"}
                  now={prediction.probability * 100}
                />
              </div>
            ))}
          </div>
        </div>
      </Card.Body>
    </Card>
  )
};

export default PredictionResult;