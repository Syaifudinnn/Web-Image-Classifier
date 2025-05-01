import React from 'react';
import { Container, Card } from 'react-bootstrap';

const About = () => {
  return (
    <Container className="py-4">
      <Card className="shadow-sm">
        <Card.Body>
          <h1 className="text-center mb-4">About This Application</h1>
          
          <h3>How It Works</h3>
          <p>
            This image classification application uses a pre-trained ResNet50 deep learning model to identify objects in 
            uploaded images. The model was trained on the ImageNet dataset, which includes over a million images across 
            1,000 different categories.
          </p>
          
          <h3>Technology Stack</h3>
          <ul>
            <li><strong>Frontend:</strong> React, React Bootstrap</li>
            <li><strong>Backend:</strong> FastAPI (Python)</li>
            <li><strong>Machine Learning:</strong> PyTorch, ResNet50 architecture</li>
          </ul>
          
          <h3>Features</h3>
          <ul>
            <li>Upload images to be classified</li>
            <li>View top 5 predictions with confidence scores</li>
            <li>Fast processing using pre-trained deep learning models</li>
          </ul>
          
          <h3>Limitations</h3>
          <p>
            The model performs best on images that contain objects similar to those in the ImageNet dataset. It may not perform 
            well on specialized domain images or images with multiple complex subjects.
          </p>
        </Card.Body>
      </Card>
    </Container>
  );
};

export default About;