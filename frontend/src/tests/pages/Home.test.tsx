import { render, screen } from '../utils/test-utils';
import Home from '../../pages/Home';

describe('Home', () => {
  it('renders the home page content', () => {
    render(<Home />);
    expect(screen.getByText('Welcome to GOTCHA')).toBeInTheDocument();
    expect(screen.getByText('The ultimate Graphical Online Turing test to Confirm Human Activity.')).toBeInTheDocument();
    expect(screen.getByText('Try it out')).toBeInTheDocument();
  });

  it('navigates to the playground when the "Try it out" button is clicked', () => {
    render(<Home />);
    const tryItOutButton = screen.getByText('Try it out');
    expect(tryItOutButton).toHaveAttribute('href', '/playground');
  });
});