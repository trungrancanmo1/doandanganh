import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import OverviewPage from "./pages/OverviewPage";
import ForgotPassword from "./pages/ForgotPassword";
import AccountSettings from "./pages/AccountSettings";
import DiseaseStatus from "./pages/DiseaseStatus";
//import PrivateRoute from "./PrivateRoute";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/overview" element={<OverviewPage />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/account-settings" element={<AccountSettings />} />
        <Route path="/disease-status" element={<DiseaseStatus />} />
      </Routes>
    </Router>
  );
}

export default App;
