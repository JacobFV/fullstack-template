import { render, screen, waitFor } from '../utils/test-utils';
import Account from '../../routes/_layout/account';

describe('Account', () => {
  it('renders the account page with user information', async () => {
    render(<Account />);
    await waitFor(() => {
      expect(screen.getByText('Account')).toBeInTheDocument();
      expect(screen.getByText('Email Verification')).toBeInTheDocument();
      expect(screen.getByText('Playground')).toBeInTheDocument();
      expect(screen.getByText('Activity History')).toBeInTheDocument();
      expect(screen.getByText('Billing')).toBeInTheDocument();
      expect(screen.getByText('API Keys')).toBeInTheDocument();
    });
  });

  it('displays the user email verification status', async () => {
    render(<Account />);
    await waitFor(() => {
      expect(screen.getByText('Your email is verified.')).toBeInTheDocument();
    });
  });

  it('navigates to the playground section', async () => {
    render(<Account />);
    await waitFor(() => {
      const playgroundLink = screen.getByText('Access the playground to test the verification system.');
      expect(playgroundLink).toHaveAttribute('href', '/playground');
    });
  });
});