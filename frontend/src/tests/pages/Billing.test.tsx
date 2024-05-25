import { render, screen, waitFor } from '../utils/test-utils';
import Billing from '../../routes/_layout/billing';

describe('Billing', () => {
  it('renders the billing page with billing history and information', async () => {
    render(<Billing />);
    await waitFor(() => {
      expect(screen.getByText('Billing')).toBeInTheDocument();
      expect(screen.getByText('Billing History')).toBeInTheDocument();
      expect(screen.getByText('Date')).toBeInTheDocument();
      expect(screen.getByText('Amount')).toBeInTheDocument();
      expect(screen.getByText('Status')).toBeInTheDocument();
      expect(screen.getByText('Billing Information')).toBeInTheDocument();
      expect(screen.getByText('Current Plan')).toBeInTheDocument();
      expect(screen.getByText('Next Billing Date')).toBeInTheDocument();
    });
  });

  it('displays the billing history items', async () => {
    render(<Billing />);
    await waitFor(() => {
      expect(screen.getByText('2023-05-01')).toBeInTheDocument();
      expect(screen.getByText('$99.99')).toBeInTheDocument();
      expect(screen.getByText('paid')).toBeInTheDocument();
    });
  });

  it('displays the current plan and next billing date', async () => {
    render(<Billing />);
    await waitFor(() => {
      expect(screen.getByText('Pro Plan')).toBeInTheDocument();
      expect(screen.getByText('2023-06-30')).toBeInTheDocument();
    });
  });
});