import { render, screen } from '../utils/test-utils';
import Navigation from '../../components/Navigation';

describe('Navigation', () => {
  it('renders the navigation menu', () => {
    render(<Navigation />);
    expect(screen.getByText('GOTCHA')).toBeInTheDocument();
    expect(screen.getByText('Account')).toBeInTheDocument();
    expect(screen.getByText('Playground')).toBeInTheDocument();
    expect(screen.getByText('Documentation')).toBeInTheDocument();
  });

  it('highlights the active link', () => {
    render(<Navigation />, { initialEntries: ['/account'] });
    expect(screen.getByText('Account')).toHaveStyle('font-weight: bold');
  });
});