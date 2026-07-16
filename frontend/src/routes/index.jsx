import { createHashRouter, RouterProvider } from 'react-router-dom';
import Layout from '../components/Layout';
import LandingPage from '../components/landing/LandingPage';
import LoginPage from '../components/auth/LoginPage';
import DashboardLayout from '../components/dashboard/DashboardLayout';
import ThreatAssessmentDashboard from '../components/dashboard/ThreatAssessmentDashboard';
import ThreatTrendsPage from '../components/dashboard/ThreatTrendsPage';
import ErrorPage from '../components/ErrorPage';

const router = createHashRouter([
  {
    path: '/',
    element: <Layout />,
    errorElement: <ErrorPage />,
    children: [
      { index: true, element: <LandingPage /> },
    ],
  },
  {
    path: '/login',
    element: <LoginPage />,
  },
  {
    path: '/dashboard',
    element: <DashboardLayout />,
    children: [
      { index: true, element: <ThreatAssessmentDashboard /> },
      { path: 'trends', element: <ThreatTrendsPage /> }
    ]
  }
]);

const Routes = () => {
  return <RouterProvider router={router} />;
};

export default Routes;
