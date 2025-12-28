import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from './App';

// Mock scrollIntoView if your chat auto-scrolls
beforeAll(() => {
  Element.prototype.scrollIntoView = jest.fn();
});

// Mock fetch globally
global.fetch = jest.fn();

beforeEach(() => {
  fetch.mockClear();
});

test('renders chat toggle button', () => {
  render(<App />);
  const button = screen.getByText(/chat/i);
  expect(button).toBeInTheDocument();
});

test('opens chat panel when toggle button is clicked', () => {
  render(<App />);
  
  const toggleButton = screen.getByText(/chat/i);
  fireEvent.click(toggleButton);

  expect(screen.getByText(/chatbot/i)).toBeInTheDocument();
  expect(screen.getByPlaceholderText(/type your question/i)).toBeInTheDocument();
});

test('sends message and displays bot response', async () => {
  // Mock successful response from backend
  fetch.mockResolvedValueOnce({
    ok: true,
    json: async () => ({ answer: 'Hello from bot!' }),
  });

  render(<App />);
  fireEvent.click(screen.getByText(/chat/i));

  const input = screen.getByPlaceholderText(/type your question/i);
  fireEvent.change(input, { target: { value: 'Hi bot' } });

  const sendButton = screen.getByText(/send/i);
  fireEvent.click(sendButton);

  // Wait for both user message and bot response to appear
  await waitFor(() => {
    expect(screen.getByText('Hi bot')).toBeInTheDocument();
    expect(screen.getByText('Hello from bot!')).toBeInTheDocument();
  });
});
