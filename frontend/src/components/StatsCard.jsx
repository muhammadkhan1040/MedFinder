import { useState, useEffect, useRef } from 'react';
import { motion, useInView } from 'framer-motion';

/**
 * StatsCard Component - Premium Redesign
 * 
 * Features:
 * - Animated counter with spring physics
 * - Gradient icon background
 * - Subtle floating animation
 * - Glass card effect
 * - Better typography hierarchy
 */
const StatsCard = ({
    icon: Icon,
    value,
    label,
    color = 'blue',
    delay = 0
}) => {
    const [displayValue, setDisplayValue] = useState(0);
    const cardRef = useRef(null);
    const isInView = useInView(cardRef, { once: true, margin: '-50px' });

    // Color configurations
    const colorConfig = {
        blue: {
            gradient: 'linear-gradient(135deg, #3B82F6 0%, #60A5FA 100%)',
            bgLight: 'rgba(59, 130, 246, 0.08)',
            shadow: '0 10px 30px -10px rgba(59, 130, 246, 0.4)',
            text: '#3B82F6',
        },
        purple: {
            gradient: 'linear-gradient(135deg, #8B5CF6 0%, #A78BFA 100%)',
            bgLight: 'rgba(139, 92, 246, 0.08)',
            shadow: '0 10px 30px -10px rgba(139, 92, 246, 0.4)',
            text: '#8B5CF6',
        },
        green: {
            gradient: 'linear-gradient(135deg, #10B981 0%, #34D399 100%)',
            bgLight: 'rgba(16, 185, 129, 0.08)',
            shadow: '0 10px 30px -10px rgba(16, 185, 129, 0.4)',
            text: '#10B981',
        },
        gold: {
            gradient: 'linear-gradient(135deg, #F59E0B 0%, #FBBF24 100%)',
            bgLight: 'rgba(245, 158, 11, 0.08)',
            shadow: '0 10px 30px -10px rgba(245, 158, 11, 0.4)',
            text: '#F59E0B',
        },
    };

    const config = colorConfig[color] || colorConfig.blue;

    // Animate counter when in view
    useEffect(() => {
        if (!isInView) return;

        const numericValue = typeof value === 'number' ? value : parseInt(value) || 0;
        const duration = 2000; // 2 seconds
        const steps = 60;
        const increment = numericValue / steps;
        let current = 0;
        let step = 0;

        const timer = setInterval(() => {
            step++;
            current = Math.min(Math.floor(increment * step), numericValue);
            setDisplayValue(current);

            if (step >= steps) {
                setDisplayValue(numericValue);
                clearInterval(timer);
            }
        }, duration / steps);

        return () => clearInterval(timer);
    }, [isInView, value]);

    // Format number with commas
    const formatNumber = (num) => {
        return num.toLocaleString('en-US');
    };

    return (
        <motion.div
            ref={cardRef}
            initial={{ opacity: 0, y: 30 }}
            animate={isInView ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.5, delay, ease: 'easeOut' }}
            whileHover={{
                y: -8,
                boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.15)',
            }}
            style={{
                background: 'white',
                borderRadius: '20px',
                padding: '1.75rem',
                boxShadow: '0 4px 20px -5px rgba(0, 0, 0, 0.08)',
                border: '1px solid #F1F5F9',
                transition: 'all 0.3s ease',
                cursor: 'default',
            }}
        >
            {/* Icon with Gradient Background */}
            <motion.div
                animate={{
                    y: [0, -5, 0],
                }}
                transition={{
                    duration: 3,
                    repeat: Infinity,
                    ease: 'easeInOut',
                    delay: delay * 2,
                }}
                style={{
                    display: 'inline-flex',
                    padding: '1rem',
                    background: config.gradient,
                    borderRadius: '16px',
                    marginBottom: '1.25rem',
                    boxShadow: config.shadow,
                }}
            >
                <Icon size={28} style={{ color: 'white' }} />
            </motion.div>

            {/* Value */}
            <div style={{
                marginBottom: '0.5rem',
            }}>
                <motion.span
                    style={{
                        fontFamily: "'JetBrains Mono', monospace",
                        fontSize: '2.5rem',
                        fontWeight: 700,
                        background: config.gradient,
                        WebkitBackgroundClip: 'text',
                        WebkitTextFillColor: 'transparent',
                        backgroundClip: 'text',
                        lineHeight: 1,
                    }}
                >
                    {formatNumber(displayValue)}
                </motion.span>
                <motion.span
                    initial={{ opacity: 0, scale: 0.5 }}
                    animate={isInView ? { opacity: 1, scale: 1 } : {}}
                    transition={{ delay: delay + 0.5, duration: 0.3 }}
                    style={{
                        fontSize: '1.5rem',
                        color: config.text,
                        marginLeft: '0.25rem',
                    }}
                >
                    +
                </motion.span>
            </div>

            {/* Label */}
            <p style={{
                fontSize: '0.9375rem',
                fontWeight: 500,
                color: '#64748B',
                margin: 0,
            }}>
                {label}
            </p>

            {/* Decorative Gradient Bar */}
            <div style={{
                marginTop: '1.25rem',
                height: '4px',
                borderRadius: '2px',
                background: config.bgLight,
                overflow: 'hidden',
            }}>
                <motion.div
                    initial={{ width: 0 }}
                    animate={isInView ? { width: '100%' } : {}}
                    transition={{ duration: 1, delay: delay + 0.3, ease: 'easeOut' }}
                    style={{
                        height: '100%',
                        background: config.gradient,
                        borderRadius: '2px',
                    }}
                />
            </div>
        </motion.div>
    );
};

export default StatsCard;
