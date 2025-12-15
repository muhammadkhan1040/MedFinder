import { useState } from 'react';
import { motion } from 'framer-motion';
import {
    Pill, Building2, Tag, CheckCircle, XCircle,
    Search, Scale, Loader2, ExternalLink, Sparkles
} from 'lucide-react';

/**
 * MedicineCard Component - Premium Redesign
 * 
 * Features:
 * - Glassmorphism card with gradient border on hover
 * - Smooth 3D lift animation on hover
 * - Prominent price display with gradient
 * - Animated savings badge
 * - Better visual hierarchy
 * - Premium button styling
 */
const MedicineCard = ({
    medicine,
    onViewDetails,
    onCheckStock,
    onCompare,
    showSavings = false,
    savingsPercent = 0,
    isSelected = false,
    index = 0
}) => {
    const [isCheckingStock, setIsCheckingStock] = useState(false);
    const [availability, setAvailability] = useState(null);
    const [isHovered, setIsHovered] = useState(false);

    const handleCheckStock = async () => {
        if (onCheckStock) {
            setIsCheckingStock(true);
            try {
                const result = await onCheckStock(medicine);
                setAvailability(result);
            } finally {
                setIsCheckingStock(false);
            }
        }
    };

    // Format price properly
    const formatPrice = (priceStr) => {
        if (!priceStr || priceStr === 'N/A') return 'N/A';

        // If already formatted with Rs., return as is
        if (typeof priceStr === 'string' && priceStr.includes('Rs.')) {
            return priceStr;
        }

        // Extract numeric value
        const numericPrice = parseFloat(String(priceStr).replace(/[^0-9.]/g, ''));
        if (isNaN(numericPrice)) return 'N/A';

        return `Rs. ${numericPrice.toFixed(2)}`;
    };

    const name = medicine?.name || 'Unknown Medicine';
    const brand = medicine?.brand || 'Unknown Brand';
    const price = formatPrice(medicine?.price);
    const composition = medicine?.composition || 'N/A';
    const categories = medicine?.categories || [];

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: index * 0.05, ease: 'easeOut' }}
            whileHover={{ y: -8 }}
            onHoverStart={() => setIsHovered(true)}
            onHoverEnd={() => setIsHovered(false)}
            style={{
                position: 'relative',
                background: 'white',
                borderRadius: '20px',
                padding: '1.5rem',
                boxShadow: isHovered
                    ? '0 25px 50px -12px rgba(0, 0, 0, 0.15)'
                    : '0 4px 6px -1px rgba(0, 0, 0, 0.07), 0 2px 4px -2px rgba(0, 0, 0, 0.05)',
                border: isSelected
                    ? '2px solid #8B5CF6'
                    : isHovered
                        ? '2px solid rgba(59, 130, 246, 0.3)'
                        : '2px solid #F1F5F9',
                overflow: 'hidden',
                transition: 'all 0.3s ease',
            }}
        >
            {/* Gradient Border Effect on Hover */}
            {isHovered && (
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    style={{
                        position: 'absolute',
                        inset: 0,
                        borderRadius: '20px',
                        padding: '2px',
                        background: 'linear-gradient(135deg, #3B82F6 0%, #8B5CF6 50%, #EC4899 100%)',
                        WebkitMask: 'linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0)',
                        WebkitMaskComposite: 'xor',
                        maskComposite: 'exclude',
                        pointerEvents: 'none',
                    }}
                />
            )}

            {/* Savings Badge */}
            {showSavings && savingsPercent > 0 && (
                <motion.div
                    initial={{ scale: 0, rotate: -10 }}
                    animate={{ scale: 1, rotate: 0 }}
                    transition={{ type: 'spring', damping: 15 }}
                    style={{
                        position: 'absolute',
                        top: '-4px',
                        right: '-4px',
                        zIndex: 10,
                    }}
                >
                    <div style={{
                        background: 'linear-gradient(135deg, #F59E0B 0%, #F97316 100%)',
                        color: 'white',
                        padding: '0.375rem 0.875rem',
                        borderRadius: '0 16px 0 16px',
                        fontWeight: 700,
                        fontSize: '0.8rem',
                        boxShadow: '0 4px 15px rgba(245, 158, 11, 0.4)',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '0.25rem',
                    }}>
                        <Sparkles size={14} />
                        Save {savingsPercent.toFixed(0)}%
                    </div>
                </motion.div>
            )}

            {/* Header */}
            <div style={{
                display: 'flex',
                alignItems: 'flex-start',
                gap: '0.875rem',
                marginBottom: '1rem',
            }}>
                {/* Icon */}
                <motion.div
                    animate={{
                        rotate: isHovered ? [0, -5, 5, 0] : 0,
                    }}
                    transition={{ duration: 0.5 }}
                    style={{
                        padding: '0.75rem',
                        background: 'linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%)',
                        borderRadius: '14px',
                        flexShrink: 0,
                    }}
                >
                    <Pill
                        size={24}
                        style={{
                            color: '#3B82F6',
                        }}
                    />
                </motion.div>

                {/* Title & Brand */}
                <div style={{ flex: 1, minWidth: 0 }}>
                    <h3 style={{
                        fontWeight: 600,
                        fontSize: '1.0625rem',
                        color: '#1E293B',
                        marginBottom: '0.25rem',
                        overflow: 'hidden',
                        textOverflow: 'ellipsis',
                        whiteSpace: 'nowrap',
                    }} title={name}>
                        {name}
                    </h3>
                    <div style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '0.375rem',
                        color: '#64748B',
                        fontSize: '0.8125rem',
                    }}>
                        <Building2 size={14} />
                        <span style={{
                            overflow: 'hidden',
                            textOverflow: 'ellipsis',
                            whiteSpace: 'nowrap',
                        }}>{brand}</span>
                    </div>
                </div>
            </div>

            {/* Price */}
            <div style={{
                textAlign: 'center',
                padding: '1rem',
                marginBottom: '1rem',
                background: 'linear-gradient(135deg, #F8FAFC 0%, #EFF6FF 100%)',
                borderRadius: '12px',
                border: '1px solid #E2E8F0',
            }}>
                <span style={{
                    fontFamily: "'JetBrains Mono', monospace",
                    fontSize: '1.5rem',
                    fontWeight: 700,
                    background: 'linear-gradient(135deg, #1E293B 0%, #475569 100%)',
                    WebkitBackgroundClip: 'text',
                    WebkitTextFillColor: 'transparent',
                    backgroundClip: 'text',
                }}>
                    {price}
                </span>
            </div>

            {/* Composition */}
            <div style={{ marginBottom: '1rem' }}>
                <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.375rem',
                    marginBottom: '0.375rem',
                    color: '#94A3B8',
                    fontSize: '0.6875rem',
                    textTransform: 'uppercase',
                    letterSpacing: '0.05em',
                    fontWeight: 600,
                }}>
                    <Tag size={12} />
                    <span>Composition</span>
                </div>
                <p style={{
                    fontSize: '0.8125rem',
                    color: '#475569',
                    lineHeight: 1.5,
                    display: '-webkit-box',
                    WebkitLineClamp: 2,
                    WebkitBoxOrient: 'vertical',
                    overflow: 'hidden',
                }} title={composition}>
                    {composition}
                </p>
            </div>

            {/* Categories */}
            {categories.length > 0 && (
                <div style={{
                    display: 'flex',
                    flexWrap: 'wrap',
                    gap: '0.375rem',
                    marginBottom: '1rem',
                }}>
                    {categories.slice(0, 3).map((cat, i) => (
                        <span
                            key={i}
                            style={{
                                padding: '0.25rem 0.625rem',
                                background: 'rgba(59, 130, 246, 0.08)',
                                color: '#3B82F6',
                                fontSize: '0.6875rem',
                                fontWeight: 500,
                                borderRadius: '9999px',
                            }}
                        >
                            {cat}
                        </span>
                    ))}
                    {categories.length > 3 && (
                        <span style={{
                            padding: '0.25rem 0.625rem',
                            background: '#F1F5F9',
                            color: '#64748B',
                            fontSize: '0.6875rem',
                            fontWeight: 500,
                            borderRadius: '9999px',
                        }}>
                            +{categories.length - 3}
                        </span>
                    )}
                </div>
            )}

            {/* Availability Status */}
            {availability !== null && (
                <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '0.5rem',
                        marginBottom: '1rem',
                        padding: '0.75rem',
                        borderRadius: '10px',
                        background: availability === 1
                            ? 'rgba(16, 185, 129, 0.1)'
                            : 'rgba(239, 68, 68, 0.1)',
                        border: availability === 1
                            ? '1px solid rgba(16, 185, 129, 0.2)'
                            : '1px solid rgba(239, 68, 68, 0.2)',
                        color: availability === 1 ? '#059669' : '#DC2626',
                    }}
                >
                    {availability === 1 ? (
                        <>
                            <CheckCircle size={18} />
                            <span style={{ fontWeight: 600, fontSize: '0.875rem' }}>In Stock</span>
                        </>
                    ) : (
                        <>
                            <XCircle size={18} />
                            <span style={{ fontWeight: 600, fontSize: '0.875rem' }}>Out of Stock</span>
                        </>
                    )}
                </motion.div>
            )}

            {/* Actions */}
            <div style={{
                display: 'flex',
                gap: '0.5rem',
                paddingTop: '1rem',
                borderTop: '1px solid #F1F5F9',
            }}>
                {/* Details Button */}
                <motion.button
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={() => onViewDetails?.(medicine)}
                    style={{
                        flex: 1,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        gap: '0.375rem',
                        padding: '0.625rem',
                        background: 'transparent',
                        color: '#3B82F6',
                        border: '1.5px solid rgba(59, 130, 246, 0.3)',
                        borderRadius: '10px',
                        fontSize: '0.8125rem',
                        fontWeight: 600,
                        cursor: 'pointer',
                        transition: 'all 0.2s ease',
                    }}
                    onMouseEnter={(e) => {
                        e.currentTarget.style.background = 'rgba(59, 130, 246, 0.05)';
                        e.currentTarget.style.borderColor = '#3B82F6';
                    }}
                    onMouseLeave={(e) => {
                        e.currentTarget.style.background = 'transparent';
                        e.currentTarget.style.borderColor = 'rgba(59, 130, 246, 0.3)';
                    }}
                >
                    <Search size={14} />
                    Details
                </motion.button>

                {/* Stock Button */}
                <motion.button
                    whileHover={{ scale: 1.02, boxShadow: '0 4px 15px rgba(16, 185, 129, 0.3)' }}
                    whileTap={{ scale: 0.98 }}
                    onClick={handleCheckStock}
                    disabled={isCheckingStock}
                    style={{
                        flex: 1,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        gap: '0.375rem',
                        padding: '0.625rem',
                        background: 'linear-gradient(135deg, #10B981 0%, #34D399 100%)',
                        color: 'white',
                        border: 'none',
                        borderRadius: '10px',
                        fontSize: '0.8125rem',
                        fontWeight: 600,
                        cursor: isCheckingStock ? 'wait' : 'pointer',
                        opacity: isCheckingStock ? 0.7 : 1,
                        transition: 'all 0.2s ease',
                    }}
                >
                    {isCheckingStock ? (
                        <Loader2 size={14} className="animate-spin" />
                    ) : (
                        <CheckCircle size={14} />
                    )}
                    {isCheckingStock ? 'Checking...' : 'Stock'}
                </motion.button>

                {/* Compare Button */}
                <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => onCompare?.(medicine)}
                    style={{
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        padding: '0.625rem',
                        background: isSelected
                            ? 'linear-gradient(135deg, #8B5CF6 0%, #A78BFA 100%)'
                            : 'transparent',
                        color: isSelected ? 'white' : '#8B5CF6',
                        border: isSelected ? 'none' : '1.5px solid rgba(139, 92, 246, 0.3)',
                        borderRadius: '10px',
                        cursor: 'pointer',
                        transition: 'all 0.2s ease',
                    }}
                    onMouseEnter={(e) => {
                        if (!isSelected) {
                            e.currentTarget.style.background = 'rgba(139, 92, 246, 0.05)';
                            e.currentTarget.style.borderColor = '#8B5CF6';
                        }
                    }}
                    onMouseLeave={(e) => {
                        if (!isSelected) {
                            e.currentTarget.style.background = 'transparent';
                            e.currentTarget.style.borderColor = 'rgba(139, 92, 246, 0.3)';
                        }
                    }}
                >
                    <Scale size={14} />
                </motion.button>
            </div>
        </motion.div>
    );
};

export default MedicineCard;
