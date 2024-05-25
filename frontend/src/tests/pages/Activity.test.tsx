import { render, screen, waitFor } from '../utils/test-utils';
import Activity from '../../pages/Activity';

describe('Activity', () => {
  it('renders the activity page with verification history', async () => {
    render(<Activity />);
    await waitFor(() => {
      expect(screen.getByText('Activity')).toBeInTheDocument();
      expect(screen.getByText('Date')).toBeInTheDocument();
      expect(screen.getByText('Verification ID')).toBeInTheDocument();
      expect(screen.getByText('Status')).toBeInTheDocument();
    });
  });

  it('displays the verification history items', async () => {
    render(<Activity />);
    await waitFor(() => {
      expect(screen.getByText('2023-06-01')).toBeInTheDocument();
      expect(screen.getByText('123456')).toBeInTheDocument();
      expect(screen.getByText('approved')).toBeInTheDocument();
    });
  });
});