import { Outlet } from 'react-router-dom';

const Layout = () => {
  return (
    <>
      {/* Header */}
      <header className='bg-[#09090B/80] backdrop-blur-sm border-b border-[#111113/30]'>
        <div className='max-w-7xl mx-auto px-4 sm:px-6 lg:px-8'>
          <div className='flex justify-between h-16'>
            <div className='flex'>
              <div className='flex-shrink-0 flex items-center'>
                <span className='text-xl font-bold text-white'>
                  <span className='text-[#00E5FF]'>Scam</span><span className='text-white'>Mirror</span>
                </span>
              </div>
              <div className='hidden md:block'>
                <div className='ml-10 flex items-baseline space-x-4'>
                  <a href='#' className='px-3 py-2 rounded-md text-sm font-medium text-gray-300 hover:text-white hover:bg-[#111113/30]'>
                    Home
                  </a>
                  <a href='#' className='px-3 py-2 rounded-md text-sm font-medium text-gray-300 hover:text-white hover:bg-[#111113/30]'>
                    About
                  </a>
                  <a href='#' className='px-3 py-2 rounded-md text-sm font-medium text-gray-300 hover:text-white hover:bg-[#111113/30]'>
                    Blog
                  </a>
                </div>
              </div>
            </div>
            <div className='hidden md:block'>
              <div className='ml-4 flex items-center md ml-0'>
                {/* Dark mode toggle would go here */}
                <button className='bg-[#111113/30] hover:bg-[#111113/40] text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm flex items-center'>
                  <span className='mr-1'>🌙</span>
                  <span className='sr-only'>Toggle dark mode</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </header>

      <main className='min-h-screen bg-gradient-to-br from-[#09090B] to-[#111113]'>
        <Outlet />
      </main>

      {/* Footer */}
      <footer className='bg-[#09090B/80] backdrop-blur-sm border-t border-[#111113/30]'>
        <div className='max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8'>
          <div className='grid grid-cols-1 md:grid-cols-3 gap-8 text-gray-400'>
            <div>
              <h3 className='text-white font-semibold mb-4'>ScamMirror AI</h3>
              <p className='text-sm'>
                Protecting users from scams through AI-powered threat intelligence.
              </p>
            </div>
            <div>
              <h3 className='text-white font-semibold mb-4'>Resources</h3 className ' ' '  >  >' a > ,  :  '  \  \  \  \  \  \  \  \  \  \  \  \  \  \  \  \  \  \  \  \  \  \  \  \  \  \  \  \  \  \  \  \  \  \  \  \  \  \  \<
  <  \className'  <
/div>
              <div>
                <h3 className='text-white font-semibold mb-4'>Quick Links</h3>
                <ul className='space-y-2'>
                  <li><a href='#' className='hover:text-white'>How It Works</a></li>
                  <li><a href='#' className='hover:text-white'>Security Blog</a></li>
                  <li><a href='#' className='hover:text-white'>Report a Scam</a></li>
                  <li><a href='#' className='hover:text-white'>Privacy Policy</a></li>
                  <li><a href='#' className='hover:text-white'>Terms of Service</a></li>
                </ul>
              </div>
              <div>
                <h3 className='text-white font-semibold mb-4'>Stay Protected</h3>
                <p className='text-sm'>
                  Follow us for the latest scam alerts and protection tips:
                </p>
                <div className='flex space-x-4 mt-3'>
                  <a href='#' className='text-gray-400 hover:text-white px-3 py-1 rounded hover:bg-[#111113/30]'>
                    <span className='mr-1'>🐦</span>Twitter
                  </a>
                  <a href='#' className='text-gray-400 hover:text-white px-3 py-1 rounded hover:bg-[#111113/30]'>
                    <span className='mr-1'>📘</span>Facebook
                  </a>
                  <a href='#' className='text-gray-400 hover:text-white px-3 py-1 rounded hover:bg-[#111113/30]'>
                    <span className='mr-1'>📸</span>Instagram
                  </a>
                </div>
              </div>
            </div>
          </div>
          <div className='mt-10 pt-8 border-t border-[#111113/30] text-center text-sm text-gray-500'>
            <p>&copy; 2026 ScamMirror AI. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </>
  );
};

export default Layout;