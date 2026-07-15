import { createHashRouter, RouterProvider } from 'react-router-dom';
import Layout from '../components/Layout';
import Homepage from '../components/Homepage';
// Placeholder for future pages
// import History from '../components/History';

const router = createHashRouter([
  {
    path: '/',
    element: <Layout />,
    children: [
      { index: true, element: <Homepage /> },
      // { path: 'history', element: <History /> },
    ],
  },
]);

const Routes = () => {
  return <RouterProvider router={router} />;
};

export default Routes;
