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
                <span className='text-2xl font-bold text-white bg-clip-text text-transparent bg-gradient-to-r from-[#00E5FF] to-[#00BFA6]'>
                  <span className='bg-transparent'>Scam</span><span className='bg-transparent'>Mirror</span>
                </span>
              </div>
              <div className='hidden md:block'>
                <div className='ml-10 flex items-baseline space-x-4'>
                  <a href='#' className='px-3 py-2 rounded-md text-sm font-medium text-gray-300 hover:text-white hover:bg-[#111113/30] transition-all duration-200'>
                    Home
                  </a>
                  <a href='#' className='px-3 py-2 rounded-md text-sm font-medium text-gray-300 hover:text-white hover:bg-[#111113/30] transition-all duration-200'>
                    About
                  </a>
                  <a href='#' className='px-3 py-2 rounded-md text-sm font-medium text-gray-300 hover:text-white hover:bg-[#111113/30] transition-all duration-200'>
                    Blog
                  </a>
                </div>
              </div>
            </div>
            <div className='hidden md:block'>
              <div className='ml-4 flex items-center md ml-0'>
                {/* Dark mode toggle would go here */}
                <button className='bg-[#111113/30] hover:bg-[#111113/40] text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm flex items-center transition-all duration-200 transform hover:scale-105'>
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
        <div className='max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12'>
          <div className='grid gap-8 text-gray-400'>
            <div className='md:col-span-2'>
              <h3 className='text-white font-bold text-xl mb-6'>ScamMirror AI</h3>
              <p className='text-sm leading-relaxed'>
                Protecting users from scams through AI-powered threat intelligence. Our mission is to create a safer digital world by providing real-time scam detection and community-driven threat intelligence.
              </p>
            </div>
            <div className='grid grid-cols-2 gap-4'>
              <div>
                <h4 className='text-white font-semibold mb-3'>Resources</h4>
                <ul className='space-y-2'>
                  <li><a href='#' className='hover:text-white transition-colors duration-200'>How It Works</a></li>
                  <li><a href='#' className='hover:text-white transition-colors duration-200'>Security Blog</a></li>
                  <li><a href='#' className='hover:text-white transition-colors duration-200'>Report a Scam</a></li>
                  <li><a href='#' className='hover:text-white transition-colors duration-200'>Privacy Policy</a></li>
                  <li><a href='#' className='hover:text-white transition-colors duration-200'>Terms of Service</a></li>
                </ul>
              </div>
              <div>
                <h4 className='text-white font-semibold mb-3'>Company</h4>
                <ul className='space-y-2'>
                  <li><a href='#' className='hover:text-white transition-colors duration-200'>About Us</a></li>
                  <li><a href='#' className='hover:text-white transition-colors duration-200'>Careers</a></li>
                  <li><a href='#' className='hover:text-white transition-colors duration-200'>Press</a></li>
                  <li><a href='#' className='hover:text-white transition-colors duration-200'>Contact</a></li>
                </ul>
              </div>
              <div>
                <h4 className='text-white font-semibold mb-3'>Legal</h4>
                <ul className='space-y-2'>
                  <li><a href='#' className='hover:text-white transition-colors duration-200'>Security</a></li>
                  <li><a href='#' className='hover:text-white transition-colors duration-200'>Compliance</a></li>
                  <li><a href='#' className='hover:text-white transition-colors duration-200'>Accessibility</a></li>
                  <li><a href='#' className='hover:text-white transition-colors duration-200'>Cookie Policy</a></li>
                </ul>
              </div>
            </div>
            <div className='border-l pl-6'>
              <h4 className='text-white font-semibold mb-3'>Stay Protected</h4>
              <p className='text-sm mb-4'>
                Follow us for the latest scam alerts and protection tips:
              </p>
              <div className='flex space-x-4'>
                <a href='#' className='p-3 rounded-full bg-[#111113/30] hover:bg-[#1] hover:bg-[#111113/40] transition-all duration-300 transform hover:-translate-y-1'>
                  <span className='text-xl'>🐦</span>
                </a>
                <a href='#' className='p-3 rounded-full bg-[#111113/30] hover:bg-[#111113/40] transition-all duration-300 transform hover:-translate-y-1'>
                  <span className='text-xl'>📘</span>
                </a>
                <a href='#' className='p-3 rounded-full bg-[#111113/30] hover:bg-[#111113/40] transition-all duration-300 transform hover:-translate-y-1'>
                  <span className='text-xl'>📸</span>
                </a>
                <a href='#' className='p-3 rounded-full bg-[#111113/30] hover:bg-[#111113/40] transition-all duration-300 transform hover:-translate-y-1'>
                  <span className='text-xl'>💬</span>
                </a>
              </div>
            </div>
          </div>
          <div className='mt-12 pt-8 border-t border-[#111113/30] text-center text-sm text-gray-500'>
            <p>&copy; 2026 ScamMirror AI. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </>
  );
};

export default Layout;