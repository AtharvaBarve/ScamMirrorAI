import React from 'react';

const SkeletonLoader = ({
  className = '',
  style = {},
  height = 20,
  width = '100%',
  borderRadius = 4,
  margin = '4px 0'
}) => {
  return (
    <div
      className={`${className} animate-pulse`}
      style={{
        backgroundColor: 'rgba(255, 255, 255, 0.05)',
        borderRadius: `${borderRadius}px`,
        height: `${height}px`,
        width: width,
        margin,
        ...style
      }}
    />
  );
};

export default SkeletonLoader;