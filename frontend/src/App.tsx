import React from 'react';
import { Box } from '@chakra-ui/react';
import { Route, Routes } from 'react-router-dom';
import Navigation from './components/Navigation';
import Footer from './components/Footer';
import Home from './routes/_layout/home';
import Login from './routes/_layout/login-bad';
import Register from './routes/_layout/register';
import ForgotPassword from './routes/_layout/forgot-password';
import ResetPassword from './routes/_layout/reset-password-bad';
import Account from './routes/_layout/account';
import Playground from './routes/_layout/playground';
import Activity from './routes/_layout/activity';
import Billing from './routes/_layout/billing';
import APIKeys from './routes/_layout/api-keys';
import Settings from './routes/_layout/settings-bad';
import Verification from './routes/_layout/verification';
import PrivacyPolicy from './routes/_layout/privacy-policy';
import TermsOfService from './routes/_layout/terms-of-service';

const App: React.FC = () => {
  return (
    <Box>
      <Navigation />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/reset-password" element={<ResetPassword />} />
        <Route path="/account" element={<Account />} />
        <Route path="/playground" element={<Playground />} />
        <Route path="/activity" element={<Activity />} />
        <Route path="/billing" element={<Billing />} />
        <Route path="/api-keys" element={<APIKeys />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="/verification" element={<Verification />} />
        <Route path="/privacy-policy" element={<PrivacyPolicy />} />
        <Route path="/terms-of-service" element={<TermsOfService />} />
      </Routes>
      <Footer />
    </Box>
  );
};

export default App;