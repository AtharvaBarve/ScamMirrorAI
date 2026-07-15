import React, { useState } from 'react';

const ProtectOthersSection = ({ result }) => {
  const [showModal, setShowModal] = useState(false);
  const [showConfirmation, setShowConfirmation] = useState(false);

  const handleReportClick = () => {
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setShowConfirmation(false);
  };

  const handleConfirmReport = () => {
    // In a real implementation, this would send an anonymous report to the backend
    setShowModal(false);
    setShowConfirmation(true);
  };

  const handleShareWarning = () => {
    // Create a shareable warning message
    const warningMessage = `⚠️ SCAM ALERT: ${result.verdict}\n\n${result.explanation}\n\n#ScamAlert #StaySafe`;

    // Try to use the Web Share API if available
    if (navigator.share) {
      navigator.share({
        title: 'Scam Alert - ScamMirror AI',
        text: warningMessage,
      }).catch(() => {
        // Fallback to copying if share fails
        navigator.clipboard.writeText(warningMessage).then(() => {
          alert('Warning copied to clipboard! Share it manually.');
        });
      });
    } else {
      // Fallback to copying
      navigator.clipboard.writeText(warningMessage).then(() => {
        alert('Warning copied to clipboard! Share it manually.');
      });
    }
  };

  const handleCopyWarning = () => {
    const warningMessage = `⚠️ SCAM ALERT: ${result.verdict}\n\n${result.explanation}\n\n#ScamAlert #StaySafe`;

    navigator.clipboard.writeText(warningMessage).then(() => {
      alert('Warning copied to clipboard!');
    }).catch(() => {
      alert('Failed to copy to clipboard');
    });
  };

  return (
    <>
      <div className='bg-[#111113/50] backdrop-blur-sm rounded-2xl border border-[#111113/30] p-6'>
        <h3 className='text-xl font-bold text-white flex items-center mb-4'>
          <span className='mr-2'>🛡️</span>
          Protect Others
        </h3>

        <p className='text-gray-300 mb-4'>
          Help protect others by reporting this scam anonymously. Your report will contribute to our community threat intelligence and help prevent others from falling victim.
        </p>

        <div className='space-y-3'>
          <button
            onClick={handleReportClick}
            className='w-full bg-gradient-to-r from-[#FF4D6D] to-[#FF9E8D] hover:from-[#FF6B8B] hover:to-[#FFB7A0] text-white font-bold py-3 px-6 rounded-lg flex items-center justify-center gap-2 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1'
          >
            <span className='mr-2'>📝</span>
            Report Scam Anonymously
          </button>

          <div className='flex space-x-2'>
            <button
              onClick={handleShareWarning}
              className='flex-1 bg-gradient-to-r from-[#6366F1] to.[4f46e5] hover:from-[7c3aed] hover:to-[6366f1] text-white font-bold py-3 px-4 rounded-lg flex items-center justify-center gap-2 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1'
            >
              <span className='mr-2'>📤</span>
              Share Warning
            </button>

            <button
              onClick={handleCopyWarning}
              className='flex-1 bg-gradient-to-r from-[#10b981] to.[059669] hover:from-[34d399] hover:to-[10b981] text-white font-bold py-3 px-4 rounded-lg flex items-center justify-center gap-2 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1'
            >
              <span className='mr-2'>📋</span>
              Copy Warning
            </button>
          </div>
        </div>
      </div>

      {/* Modal */}
      {showModal && (
        <div className='fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50'>
          <div className='bg-[#111113/80] backdrop-blur-sm rounded-3xl border border-[#111113/40] p-8 w-full max-w-md'>
            <div className='flex items-center justify-between mb-6'>
              <h3 className='text-xl font-bold text-white flex items-center'>
                <span className='mr-2'>📝</span>
                Report Scam Anonymously
              </h3>
              <button onClick={handleCloseModal} className='text-gray-400 hover:text-white hover:bg-[#111113/30] rounded-full p-2'>
                ✕
              </button>
            </div>

            <p className='text-gray-300 mb-6'>
              Your report will help improve our scam detection capabilities and protect others in the community. No personal information is collected or stored.
            </p>

            <div className='space-y-4'>
              <div className='flex items-center space-x-3'>
                <span className='flex-shrink-0 text-2xl'>🛡️</span>
                <div>
                  <p className='font-semibold text-white'>Anonymous Reporting</p>
                  <p className='text-gray-400 text-sm'>
                    Your identity remains completely private
                  </p>
                </div>
              </div>

              <div className='flex items-center space-x-3'>
                <span className='flex-shrink-0 text-2xl'>📊</span>
                <div>
                  <p className='font-semibold text-white'>Community Protection</p>
                  <p className='text-gray-400 text-sm'>
                    Helps improve threat detection for everyone
                  </p>
                </div>
              </div>

              <div className='flex items-center space-x-3'>
                <span className='flex-shrink-0 text-2xl'>⚡</span>
                <div>
                  <p className='font-semibold text-white'>Immediate Impact</p>
                  <p className='text-gray-400 text-sm'>
                    Reported threats are analyzed in real-time
                  </p>
                </div>
              </div>
            </div>

            <div className='mt-8 pt-4 border-t border-[#111113/20]'>
              <button
                onClick={handleConfirmReport}
                className='w-full bg-gradient-to-r from-[#22C55E] to.[16a34a] hover:from-[34d399] hover:to-[22c55e] text-white font-bold py-3 px-6 rounded-lg flex items-center justify-center gap-2 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1'
              >
                <span className='mr-2'>✅</span>
                Submit Anonymous Report
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Confirmation */}
      {showConfirmation && (
        <div className='fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50'>
          <div className='bg-[#111113/80] backdrop-blur-sm rounded-3xl border border-[#111113/40] p-8 text-center max-w-md'>
            <div className='space-y-6'>
              <div className='flex items-center justify-center mb-4'>
                <span className='text-4xl text-[#22C55E]'>✅</span>
              </div>
              <h3 className='font-bold text-white mb-3'>
                Thank you.
              </h3>
              <p className='text-gray-300'>
                Your anonymous report helps identify scam campaigns and protect future users.
              </p>
              <button
                onClick={handleCloseModal}
                className='w-full bg-gradient-to-r from.[22C55E] to.[16a34a] hover:from-[34d399] hover:to-[22c55e] text-white font-bold py-3 px-6 rounded-lg flex items-center justify-center gap-2 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1'
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default ProtectOthersSection;