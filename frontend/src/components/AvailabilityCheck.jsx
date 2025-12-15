import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { CheckCircle, XCircle, Clock, Loader2, RefreshCw, ExternalLink } from 'lucide-react';
import { checkAvailability } from '../api/medfinder';
import { getRelativeTime } from '../utils/debounce';

/**
 * AvailabilityCheck Component
 * 
 * Features:
 * - Large status indicator (green/red/yellow)
 * - Status text matches circle color
 * - Loading state with pulse animation
 * - "Last checked" timestamp
 * - Cache indicator
 */
const AvailabilityCheck = ({
    medicineName,
    autoCheck = false,
    onResult
}) => {
    const [status, setStatus] = useState(null); // null | 'loading' | 'available' | 'unavailable' | 'unknown'
    const [lastChecked, setLastChecked] = useState(null);
    const [isFromCache, setIsFromCache] = useState(false);
    const [error, setError] = useState(null);

    const performCheck = async () => {
        if (!medicineName) return;

        setStatus('loading');
        setError(null);

        try {
            const startTime = Date.now();
            const result = await checkAvailability(medicineName);
            const duration = Date.now() - startTime;

            // If response was very fast, it's likely cached
            setIsFromCache(duration < 200);

            if (result.success) {
                if (result.available === 1) {
                    setStatus('available');
                } else if (result.available === 0) {
                    setStatus('unavailable');
                } else {
                    setStatus('unknown');
                }
                setLastChecked(new Date());
                onResult?.(result);
            } else {
                setError(result.error || 'Check failed');
                setStatus('unknown');
            }
        } catch (err) {
            setError('Network error');
            setStatus('unknown');
        }
    };

    useEffect(() => {
        if (autoCheck && medicineName) {
            performCheck();
        }
    }, [medicineName, autoCheck]);

    const getStatusConfig = () => {
        switch (status) {
            case 'available':
                return {
                    icon: CheckCircle,
                    color: 'green',
                    bgClass: 'bg-green-50 border-green-200',
                    iconClass: 'text-green-500',
                    textClass: 'text-green-700',
                    text: 'In Stock',
                    description: 'Available on dawaai.pk'
                };
            case 'unavailable':
                return {
                    icon: XCircle,
                    color: 'red',
                    bgClass: 'bg-red-50 border-red-200',
                    iconClass: 'text-red-500',
                    textClass: 'text-red-700',
                    text: 'Out of Stock',
                    description: 'Currently unavailable'
                };
            case 'unknown':
                return {
                    icon: Clock,
                    color: 'yellow',
                    bgClass: 'bg-yellow-50 border-yellow-200',
                    iconClass: 'text-yellow-500',
                    textClass: 'text-yellow-700',
                    text: 'Unknown',
                    description: 'Could not determine availability'
                };
            default:
                return null;
        }
    };

    const config = getStatusConfig();

    return (
        <div className="space-y-4">
            {/* Check Button */}
            {status !== 'loading' && (
                <button
                    onClick={performCheck}
                    disabled={!medicineName}
                    className="w-full py-3 px-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl font-semibold flex items-center justify-center gap-2 hover:shadow-lg hover:scale-[1.02] transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                >
                    <RefreshCw size={18} />
                    {status ? 'Check Again' : 'Check Availability'}
                </button>
            )}

            {/* Loading State */}
            {status === 'loading' && (
                <motion.div
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    className="p-6 bg-blue-50 border-2 border-blue-200 rounded-xl text-center"
                >
                    <motion.div
                        animate={{ scale: [1, 1.2, 1] }}
                        transition={{ duration: 1, repeat: Infinity }}
                        className="inline-block"
                    >
                        <Loader2 size={48} className="text-blue-500 animate-spin mx-auto mb-3" />
                    </motion.div>
                    <p className="text-blue-700 font-medium">Checking availability...</p>
                    <p className="text-blue-500 text-sm">This may take a moment</p>
                </motion.div>
            )}

            {/* Status Display */}
            {config && status !== 'loading' && (
                <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className={`p-6 border-2 rounded-xl ${config.bgClass}`}
                >
                    <div className="flex items-center gap-4">
                        <motion.div
                            initial={{ scale: 0 }}
                            animate={{ scale: 1 }}
                            transition={{ type: 'spring', stiffness: 200 }}
                        >
                            <config.icon size={56} className={config.iconClass} />
                        </motion.div>
                        <div className="flex-1">
                            <h3 className={`text-2xl font-bold ${config.textClass}`}>
                                {config.text}
                            </h3>
                            <p className={`${config.textClass} opacity-75`}>
                                {config.description}
                            </p>

                            {/* Last checked */}
                            {lastChecked && (
                                <div className="flex items-center gap-2 mt-2 text-sm text-gray-500">
                                    <Clock size={14} />
                                    <span>Last checked: {getRelativeTime(lastChecked)}</span>
                                    {isFromCache && (
                                        <span className="px-2 py-0.5 bg-blue-100 text-blue-600 rounded-full text-xs font-medium">
                                            ⚡ Cached
                                        </span>
                                    )}
                                </div>
                            )}
                        </div>
                    </div>

                    {/* Action buttons based on status */}
                    {status === 'available' && (
                        <a
                            href="https://dawaai.pk"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="mt-4 flex items-center justify-center gap-2 w-full py-3 bg-green-500 text-white rounded-lg font-medium hover:bg-green-600 transition-colors"
                        >
                            <ExternalLink size={18} />
                            Visit dawaai.pk to Purchase
                        </a>
                    )}

                    {status === 'unavailable' && (
                        <div className="mt-4 p-3 bg-white rounded-lg text-center">
                            <p className="text-gray-600 text-sm mb-2">
                                Medicine is currently out of stock.
                            </p>
                            <p className="text-blue-600 font-medium">
                                Check the "Alternatives" tab for similar medicines!
                            </p>
                        </div>
                    )}
                </motion.div>
            )}

            {/* Error Display */}
            {error && (
                <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-600 text-sm">
                    <strong>Error:</strong> {error}
                </div>
            )}
        </div>
    );
};

export default AvailabilityCheck;
