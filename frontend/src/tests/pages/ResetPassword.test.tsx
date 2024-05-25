import { render, screen, fireEvent, waitFor } from '../utils/test-utils';
import ResetPassword from '../../routes/_layout/reset-password-bad';

describe('ResetPassword', () => {
  it('renders the reset password form', () => {
    render(<ResetPassword />);
    expect(screen.getByLabelText('New Password')).toBeInTheDocument();
    expect(screen.getByLabelText('Confirm Password')).toBeInTheDocument();
    expect(screen.getByText('Reset Password')).toBeInTheDocument();
  });

  it('submits the reset password form with valid data', async () => {
    render(<ResetPassword />);
    const passwordInput = screen.getByLabelText('New Password');
    const confirmPasswordInput = screen.getByLabelText('Confirm Password');
    const resetButton = screen.getByText('Reset Password');

    fireEvent.change(passwordInput, { target: { value: 'newpassword123' } });
    fireEvent.change(confirmPasswordInput, { target: { value: 'newpassword123' } });
    fireEvent.click(resetButton);

    await waitFor(() => {
      expect(screen.getByText('Password reset successfully!')).toBeInTheDocument();
    });
  });

  it('displays an error message for mismatched passwords', async () => {
    render(<ResetPassword />);
    const passwordInput = screen.getByLabelText('New Password');
    const confirmPasswordInput = screen.getByLabelText('Confirm Password');
    const resetButton = screen.getByText('Reset Password');

    fireEvent.change(passwordInput, { target: { value: 'newpassword123' } });
    fireEvent.change(confirmPasswordInput, { target: { value: 'mismatchedpassword' } });
    fireEvent.click(resetButton);

    await waitFor(() => {
      expect(screen.getByText('Passwords do not match')).toBeInTheDocument();
    });
  });
});