import { motion } from 'framer-motion';

/**
 * SkeletonCard Component
 * 
 * Loading skeleton with shimmer effect
 */
const SkeletonCard = ({ className = '' }) => {
    return (
        <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className={`bg-white rounded-xl p-5 shadow-md ${className}`}
        >
            {/* Header */}
            <div className="flex items-start gap-3 mb-4">
                <div className="w-10 h-10 rounded-lg skeleton" />
                <div className="flex-1 space-y-2">
                    <div className="h-5 w-3/4 rounded skeleton" />
                    <div className="h-4 w-1/2 rounded skeleton" />
                </div>
            </div>

            {/* Price */}
            <div className="h-8 w-1/3 rounded skeleton mb-4" />

            {/* Composition */}
            <div className="space-y-2 mb-4">
                <div className="h-3 w-1/4 rounded skeleton" />
                <div className="h-4 w-full rounded skeleton" />
                <div className="h-4 w-2/3 rounded skeleton" />
            </div>

            {/* Categories */}
            <div className="flex gap-2 mb-4">
                <div className="h-6 w-16 rounded-full skeleton" />
                <div className="h-6 w-20 rounded-full skeleton" />
            </div>

            {/* Buttons */}
            <div className="flex gap-2 pt-2 border-t border-gray-100">
                <div className="flex-1 h-10 rounded-lg skeleton" />
                <div className="flex-1 h-10 rounded-lg skeleton" />
                <div className="w-10 h-10 rounded-lg skeleton" />
            </div>

            <style>{`
        .skeleton {
          background: linear-gradient(90deg, #f0f0f0 25%, #e8e8e8 50%, #f0f0f0 75%);
          background-size: 200% 100%;
          animation: shimmer 1.5s linear infinite;
        }
        @keyframes shimmer {
          0% { background-position: 200% 0; }
          100% { background-position: -200% 0; }
        }
      `}</style>
        </motion.div>
    );
};

/**
 * SkeletonText - Simple text skeleton
 */
export const SkeletonText = ({ width = '100%', height = '16px', className = '' }) => (
    <div
        className={`rounded skeleton ${className}`}
        style={{ width, height }}
    >
        <style>{`
      .skeleton {
        background: linear-gradient(90deg, #f0f0f0 25%, #e8e8e8 50%, #f0f0f0 75%);
        background-size: 200% 100%;
        animation: shimmer 1.5s linear infinite;
      }
    `}</style>
    </div>
);

/**
 * SkeletonCircle - Circular skeleton
 */
export const SkeletonCircle = ({ size = 40, className = '' }) => (
    <div
        className={`rounded-full skeleton ${className}`}
        style={{ width: size, height: size }}
    >
        <style>{`
      .skeleton {
        background: linear-gradient(90deg, #f0f0f0 25%, #e8e8e8 50%, #f0f0f0 75%);
        background-size: 200% 100%;
        animation: shimmer 1.5s linear infinite;
      }
    `}</style>
    </div>
);

export default SkeletonCard;
