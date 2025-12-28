import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import ChatbotWidget from '../Chatbot';

// Mock scrollIntoView
beforeAll(() => {
  Element.prototype.scrollIntoView = jest.fn();
});

// Mock fetch globally
global.fetch = jest.fn();

describe('ChatbotWidget', () => {
  beforeEach(() => {
    fetch.mockClear();
  });

  test('renders chatbot toggle button when closed', () => {
    render(<ChatbotWidget />);
    expect(screen.getByText('Chat')).toBeInTheDocument();
  });

  test('opens chatbot panel when toggle button is clicked', () => {
    render(<ChatbotWidget />);
    
    const toggleButton = screen.getByText('Chat');
    fireEvent.click(toggleButton);
    
    expect(screen.getByText('Chatbot')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Type your question...')).toBeInTheDocument();
  });

  test('sends message when send button is clicked', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ answer: 'Test response from server' })
    });

    render(<ChatbotWidget />);
    fireEvent.click(screen.getByText('Chat'));

    const input = screen.getByPlaceholderText('Type your question...');
    fireEvent.change(input, { target: { value: 'Test question' } });

    const sendButton = screen.getByText('Send');
    fireEvent.click(sendButton);

    await waitFor(() => {
      expect(screen.getByText('Test question')).toBeInTheDocument();
      expect(screen.getByText('Test response from server')).toBeInTheDocument();
    });
  });

  // ... other tests remain unchanged
});
