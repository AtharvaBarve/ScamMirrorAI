import { createHashRouter, RouterProvider } from 'react-router-dom';
import Layout from '../components/Layout';
import Analyzer from '../components/Analyzer';
// Placeholder for future pages
// import History from '../components/History';

const router = createHashRouter([
  {
    path: '/',
    element: <Layout />,
    children: [
      { index: true, element: <Analyzer /> },
      // { path: 'history', element: <History /> },
    ],
  },
]);

const Routes = () => {
  return <RouterProvider router={router} />;
};

export default Routes;