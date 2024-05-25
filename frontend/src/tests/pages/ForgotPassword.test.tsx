import { render, screen, fireEvent, waitFor } from '../utils/test-utils';
import ForgotPassword from '../../routes/_layout/forgot-password';

describe('ForgotPassword', () => {
  it('renders the forgot password form', () => {
    render(<ForgotPassword />);
    expect(screen.getByLabelText('Email address')).toBeInTheDocument();
    expect(screen.getByText('Reset Password')).toBeInTheDocument();
  });

  it('submits the forgot password form with valid email', async () => {
    render(<ForgotPassword />);
    const emailInput = screen.getByLabelText('Email address');
    const resetButton = screen.getByText('Reset Password');

    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    fireEvent.click(resetButton);

    await waitFor(() => {
      expect(screen.getByText('Password reset email sent. Please check your inbox.')).toBeInTheDocument();
    });
  });

  it('displays an error message for non-existing email', async () => {
    render(<ForgotPassword />);
    const emailInput = screen.getByLabelText('Email address');
    const resetButton = screen.getByText('Reset Password');

    fireEvent.change(emailInput, { target: { value: 'nonexisting@example.com' } });
    fireEvent.click(resetButton);

    await waitFor(() => {
      expect(screen.getByText('Email not found')).toBeInTheDocument();
    });
  });
});