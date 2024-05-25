import { render, screen } from '../utils/test-utils';
import Footer from '../../components/Footer';

describe('Footer', () => {
  it('renders the footer content', () => {
    render(<Footer />);
    expect(screen.getByText(/GOTCHA. All rights reserved/i)).toBeInTheDocument();
    expect(screen.getByText('Privacy Policy')).toBeInTheDocument();
    expect(screen.getByText('Terms of Service')).toBeInTheDocument();
  });
});