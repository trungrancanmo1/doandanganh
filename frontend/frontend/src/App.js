import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import OverviewPage from "./pages/OverviewPage";
import ForgotPassword from "./pages/ForgotPassword";
import AccountSettings from "./pages/AccountSettings";
import DiseaseStatus from "./pages/DiseaseStatus";
import DashboardLightPage from "./pages/DashboardLightInfo";
//import PrivateRoute from "./PrivateRoute";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/account-settings" element={<AccountSettings />} />
        <Route path="/dashboard/disease-status" element={<DiseaseStatus />} />
        <Route path="/dashboard/overview" element={<OverviewPage />} />
        <Route path="/dashboard/lightinfo" element={<DashboardLightPage />} />
      </Routes>
    </Router>
  );
}

export default App;
