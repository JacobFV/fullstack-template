import { render, screen, fireEvent, waitFor } from '../utils/test-utils';
import VerificationRequest from '../../pages/VerificationRequest';

describe('VerificationRequest', () => {
  it('renders the verification request page with request details', async () => {
    render(<VerificationRequest />);
    await waitFor(() => {
      expect(screen.getByText('Verification Request')).toBeInTheDocument();
      expect(screen.getByText('Request Details')).toBeInTheDocument();
      expect(screen.getByText('Purpose')).toBeInTheDocument();
      expect(screen.getByText('Required Steps')).toBeInTheDocument();
      expect(screen.getByText('Verify')).toBeInTheDocument();
      expect(screen.getByText('Decline')).toBeInTheDocument();
    });
  });

  it('displays the verification request purpose and required steps', async () => {
    render(<VerificationRequest />);
    await waitFor(() => {
      expect(screen.getByText('Identity Verification')).toBeInTheDocument();
      expect(screen.getByText('Capture photo, Provide personal information')).toBeInTheDocument();
    });
  });

  it('navigates to the verification page when "Verify" is clicked', async () => {
    render(<VerificationRequest />);
    const verifyButton = screen.getByText('Verify');
    fireEvent.click(verifyButton);

    await waitFor(() => {
      expect(window.location.pathname).toBe('/verification');
    });
  });

  it('handles declining the verification request', async () => {
    render(<VerificationRequest />);
    const declineButton = screen.getByText('Decline');
    fireEvent.click(declineButton);

    await waitFor(() => {
      expect(screen.getByText('Verification request declined')).toBeInTheDocument();
    });
  });
});