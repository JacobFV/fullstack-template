import React from 'react';
import { Box } from '@chakra-ui/react';
import { Route, Routes } from 'react-router-dom';
import Navigation from './components/Navigation';
import Footer from './components/Footer';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import ForgotPassword from './pages/ForgotPassword';
import ResetPassword from './pages/ResetPassword';
import Account from './pages/Account';
import Playground from './pages/Playground';
import Activity from './pages/Activity';
import Billing from './pages/Billing';
import APIKeys from './pages/APIKeys';
import Settings from './pages/Settings';
// import VerificationRequest from './pages/VerificationRequest';
import Verification from './pages/Verification';
import PrivacyPolicy from './pages/PrivacyPolicy';
import TermsOfService from './pages/TermsOfService';

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
        {/* <Route path="/verification-request" element={<VerificationRequest />} /> */}
        <Route path="/verification" element={<Verification />} />
        <Route path="/privacy-policy" element={<PrivacyPolicy />} />
        <Route path="/terms-of-service" element={<TermsOfService />} />
      </Routes>
      <Footer />
    </Box>
  );
};

export default App;