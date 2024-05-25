import { render, screen, fireEvent, waitFor } from '../utils/test-utils';
import APIKeys from '../../pages/APIKeys';

describe('APIKeys', () => {
  it('renders the API keys page with user API keys', async () => {
    render(<APIKeys />);
    await waitFor(() => {
      expect(screen.getByText('API Keys')).toBeInTheDocument();
      expect(screen.getByText('Your API Keys')).toBeInTheDocument();
      expect(screen.getByText('Key')).toBeInTheDocument();
      expect(screen.getByText('Created At')).toBeInTheDocument();
      expect(screen.getByText('Actions')).toBeInTheDocument();
      expect(screen.getByText('Create New API Key')).toBeInTheDocument();
    });
  });

  it('displays the user API keys', async () => {
    render(<APIKeys />);
    await waitFor(() => {
      expect(screen.getByText('abc123')).toBeInTheDocument();
      expect(screen.getByText('2023-06-01')).toBeInTheDocument();
      expect(screen.getByText('Revoke')).toBeInTheDocument();
    });
  });

  it('creates a new API key', async () => {
    render(<APIKeys />);
    const createButton = screen.getByText('Create API Key');
    fireEvent.click(createButton);
    await waitFor(() => {
      expect(screen.getByText('API key created successfully')).toBeInTheDocument();
    });
  });

  it('revokes an API key', async () => {
    render(<APIKeys />);
    const revokeButton = screen.getByText('Revoke');
    fireEvent.click(revokeButton);
    await waitFor(() => {
      expect(screen.getByText('API key revoked successfully')).toBeInTheDocument();
    });
  });
});