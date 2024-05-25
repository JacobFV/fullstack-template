import { render, screen, fireEvent, waitFor } from '../utils/test-utils';
import Settings from '../../pages/Settings';

describe('Settings', () => {
  it('renders the settings page with user information and options', async () => {
    render(<Settings />);
    await waitFor(() => {
      expect(screen.getByText('Settings')).toBeInTheDocument();
      expect(screen.getByText('User Information')).toBeInTheDocument();
      expect(screen.getByText('Name')).toBeInTheDocument();
      expect(screen.getByText('Email')).toBeInTheDocument();
      expect(screen.getByText('Change Password')).toBeInTheDocument();
      expect(screen.getByText('Export Data')).toBeInTheDocument();
      expect(screen.getByText('Delete Account')).toBeInTheDocument();
    });
  });

  it('updates user information', async () => {
    render(<Settings />);
    const nameInput = screen.getByLabelText('Name');
    const emailInput = screen.getByLabelText('Email');
    const saveButton = screen.getByText('Save Changes');

    fireEvent.change(nameInput, { target: { value: 'John Doe' } });
    fireEvent.change(emailInput, { target: { value: 'johndoe@example.com' } });
    fireEvent.click(saveButton);

    await waitFor(() => {
      expect(screen.getByText('User information updated successfully')).toBeInTheDocument();
    });
  });

  it('changes user password', async () => {
    render(<Settings />);
    const currentPasswordInput = screen.getByLabelText('Current Password');
    const newPasswordInput = screen.getByLabelText('New Password');
    const confirmPasswordInput = screen.getByLabelText('Confirm Password');
    const changePasswordButton = screen.getByText('Change Password');

    fireEvent.change(currentPasswordInput, { target: { value: 'currentpassword' } });
    fireEvent.change(newPasswordInput, { target: { value: 'newpassword' } });
    fireEvent.change(confirmPasswordInput, { target: { value: 'newpassword' } });
    fireEvent.click(changePasswordButton);

    await waitFor(() => {
      expect(screen.getByText('Password changed successfully')).toBeInTheDocument();
    });
  });

  it('exports user data', async () => {
    render(<Settings />);
    const exportDataButton = screen.getByText('Export Data');
    fireEvent.click(exportDataButton);

    await waitFor(() => {
      expect(screen.getByText('Data export initiated')).toBeInTheDocument();
    });
  });

  it('deletes user account', async () => {
    render(<Settings />);
    const deleteAccountButton = screen.getByText('Delete Account');
    fireEvent.click(deleteAccountButton);

    const confirmDeleteButton = screen.getByText('Confirm');
    fireEvent.click(confirmDeleteButton);

    await waitFor(() => {
      expect(screen.getByText('Account deleted successfully')).toBeInTheDocument();
    });
  });
});