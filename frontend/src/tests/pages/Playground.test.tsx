import { render, screen, waitFor } from '../utils/test-utils';
import Playground from '../../pages/Playground';

describe('Playground', () => {
  it('renders the playground page with embedded form and code editor', async () => {
    render(<Playground />);
    await waitFor(() => {
      expect(screen.getByText('Playground')).toBeInTheDocument();
      expect(screen.getByText('Embedded Form')).toBeInTheDocument();
      expect(screen.getByText('Playground Code')).toBeInTheDocument();
      expect(screen.getByText('API Keys')).toBeInTheDocument();
    });
  });

  it('displays the user API key', async () => {
    render(<Playground />);
    await waitFor(() => {
      expect(screen.getByText('Your API Key: abc123')).toBeInTheDocument();
    });
  });

  it('copies the playground code to clipboard', async () => {
    render(<Playground />);
    await waitFor(() => {
      const copyButton = screen.getByText('Copy Code');
      fireEvent.click(copyButton);
      expect(navigator.clipboard.writeText).toHaveBeenCalledWith('playground code');
    });
  });
});