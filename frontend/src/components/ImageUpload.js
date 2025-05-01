import React, { useState } from 'react';
import { Button, Form, Alert, Spinner } from 'react-bootstrap';
import api from '../services/api';

const ImageUpload = (props) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      // Check if file is an image
      if (!file.type.startsWith('image/')) {
        setError('Please select an image file');
        setSelectedFile(null);
        setPreview(null);
        return;
      }

      setSelectedFile(file);
      setError(null);

      // Create a preview
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedFile) {
      setError('Please select an image file');
      return;
    }

    setLoading(true);
    try {
      const result = await api.uploadImage(selectedFile);
      props.onPredictionResult(result, preview);
    } catch (error) {
      setError('Error uploading image: ' + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="m-4">
      <h2>Upload an Image</h2>
      <Form onSubmit={handleSubmit}>
        <Form.Group className="mb-3">
          <Form.Label>Select an image to classify</Form.Label>
          <Form.Control 
            type="file" 
            onChange={handleFileChange}
            accept="image/*"
          />
          <Form.Text className="text-muted">
            We'll use machine learning to identify what's in your image.
          </Form.Text>
        </Form.Group>

        {error && <Alert variant="danger">{error}</Alert>}

        {preview && (
          <div className="mb-3">
            <h5>Preview:</h5>
            <img 
              src={preview} 
              alt="Preview" 
              style={{ maxWidth: '100%', maxHeight: '300px' }} 
              className="img-thumbnail"
            />
          </div>
        )}

        <Button 
          variant="primary" 
          type="submit" 
          disabled={!selectedFile || loading}
        >
          {loading ? (
            <>
              <Spinner
                as="span"
                animation="border"
                size="sm"
                role="status"
                aria-hidden="true"
              />
              <span className="ms-2">Processing...</span>
            </>
          ) : (
            'Classify Image'
          )}
        </Button>
      </Form>
    </div>
  );
};

export default ImageUpload;