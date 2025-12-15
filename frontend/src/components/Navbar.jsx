import { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { Pill, Search, Home, FlaskConical, Menu, X, Sparkles, Phone } from 'lucide-react';

/**
 * Navbar Component - Enhanced Design
 * 
 * Features:
 * - Sticky header with glassmorphism on scroll
 * - Navigation aligned to far right
 * - Smooth transitions and hover effects
 * - Mobile responsive with slide-in menu
 * - Active link indicator with gradient underline
 */
const Navbar = () => {
    const [isScrolled, setIsScrolled] = useState(false);
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
    const location = useLocation();

    useEffect(() => {
        const handleScroll = () => {
            setIsScrolled(window.scrollY > 50);
        };

        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    // Close mobile menu on route change
    useEffect(() => {
        setIsMobileMenuOpen(false);
    }, [location.pathname]);

    const navLinks = [
        { path: '/', label: 'Home', icon: Home },
        { path: '/search', label: 'Search', icon: Search },
        { path: '/formula', label: 'Formula', icon: FlaskConical },
        { path: '/symptom-search', label: 'AI Search', icon: Sparkles },
        { path: '/prescription', label: 'Prescription', icon: Pill },
        { path: '/contact', label: 'Contact', icon: Phone },
    ];

    const isActive = (path) => location.pathname === path;

    return (
        <>
            <motion.nav
                initial={{ y: -100 }}
                animate={{ y: 0 }}
                transition={{ duration: 0.5, ease: 'easeOut' }}
                style={{
                    position: 'fixed',
                    top: 0,
                    left: 0,
                    right: 0,
                    zIndex: 200,
                    padding: isScrolled ? '0.5rem 0' : '1rem 0',
                    background: isScrolled
                        ? 'rgba(255, 255, 255, 0.85)'
                        : 'transparent',
                    backdropFilter: isScrolled ? 'blur(20px)' : 'none',
                    WebkitBackdropFilter: isScrolled ? 'blur(20px)' : 'none',
                    boxShadow: isScrolled
                        ? '0 4px 30px rgba(0, 0, 0, 0.1)'
                        : 'none',
                    borderBottom: isScrolled
                        ? '1px solid rgba(255, 255, 255, 0.3)'
                        : 'none',
                    transition: 'all 0.3s ease',
                }}
            >
                <div style={{
                    maxWidth: '1280px',
                    margin: '0 auto',
                    padding: '0 1.5rem',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                }}>
                    {/* Logo */}
                    <Link
                        to="/"
                        style={{
                            display: 'flex',
                            alignItems: 'center',
                            gap: '0.75rem',
                            textDecoration: 'none',
                        }}
                    >
                        <motion.div
                            whileHover={{ scale: 1.05, rotate: 5 }}
                            whileTap={{ scale: 0.95 }}
                            style={{
                                padding: '0.625rem',
                                borderRadius: '12px',
                                background: isScrolled
                                    ? 'linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%)'
                                    : 'rgba(255, 255, 255, 0.2)',
                                backdropFilter: 'blur(10px)',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                            }}
                        >
                            <Pill
                                size={24}
                                style={{ color: 'white' }}
                            />
                        </motion.div>
                        <span style={{
                            fontSize: '1.25rem',
                            fontWeight: 700,
                            color: isScrolled ? '#1E293B' : 'white',
                            fontFamily: "'Poppins', sans-serif",
                            letterSpacing: '-0.02em',
                        }}>
                            MedFinder
                        </span>
                    </Link>

                    {/* Desktop Navigation - Far Right */}
                    <div style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '0.5rem',
                    }} className="hidden md:flex">
                        {navLinks.map((link) => (
                            <Link
                                key={link.path}
                                to={link.path}
                                style={{
                                    display: 'flex',
                                    alignItems: 'center',
                                    gap: '0.5rem',
                                    padding: '0.625rem 1rem',
                                    borderRadius: '10px',
                                    fontWeight: 500,
                                    fontSize: '0.9rem',
                                    textDecoration: 'none',
                                    transition: 'all 0.2s ease',
                                    background: isActive(link.path)
                                        ? isScrolled
                                            ? 'linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%)'
                                            : 'rgba(255, 255, 255, 0.2)'
                                        : 'transparent',
                                    color: isActive(link.path)
                                        ? isScrolled ? '#3B82F6' : 'white'
                                        : isScrolled ? '#475569' : 'rgba(255, 255, 255, 0.85)',
                                    border: isActive(link.path)
                                        ? isScrolled
                                            ? '1px solid rgba(59, 130, 246, 0.2)'
                                            : '1px solid rgba(255, 255, 255, 0.3)'
                                        : '1px solid transparent',
                                }}
                                onMouseEnter={(e) => {
                                    if (!isActive(link.path)) {
                                        e.currentTarget.style.background = isScrolled
                                            ? 'rgba(241, 245, 249, 1)'
                                            : 'rgba(255, 255, 255, 0.15)';
                                        e.currentTarget.style.color = isScrolled ? '#1E293B' : 'white';
                                    }
                                }}
                                onMouseLeave={(e) => {
                                    if (!isActive(link.path)) {
                                        e.currentTarget.style.background = 'transparent';
                                        e.currentTarget.style.color = isScrolled ? '#475569' : 'rgba(255, 255, 255, 0.85)';
                                    }
                                }}
                            >
                                <link.icon size={18} />
                                {link.label}
                            </Link>
                        ))}
                    </div>

                    {/* Mobile Menu Button */}
                    <motion.button
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                        style={{
                            display: 'flex',
                            padding: '0.625rem',
                            borderRadius: '10px',
                            border: 'none',
                            background: isScrolled ? 'rgba(241, 245, 249, 1)' : 'rgba(255, 255, 255, 0.2)',
                            color: isScrolled ? '#475569' : 'white',
                            cursor: 'pointer',
                        }}
                        className="md:hidden"
                        aria-label="Toggle menu"
                    >
                        <AnimatePresence mode="wait">
                            {isMobileMenuOpen ? (
                                <motion.div
                                    key="close"
                                    initial={{ rotate: -90, opacity: 0 }}
                                    animate={{ rotate: 0, opacity: 1 }}
                                    exit={{ rotate: 90, opacity: 0 }}
                                    transition={{ duration: 0.2 }}
                                >
                                    <X size={24} />
                                </motion.div>
                            ) : (
                                <motion.div
                                    key="menu"
                                    initial={{ rotate: 90, opacity: 0 }}
                                    animate={{ rotate: 0, opacity: 1 }}
                                    exit={{ rotate: -90, opacity: 0 }}
                                    transition={{ duration: 0.2 }}
                                >
                                    <Menu size={24} />
                                </motion.div>
                            )}
                        </AnimatePresence>
                    </motion.button>
                </div>
            </motion.nav>

            {/* Mobile Menu Overlay */}
            <AnimatePresence>
                {isMobileMenuOpen && (
                    <>
                        {/* Backdrop */}
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            onClick={() => setIsMobileMenuOpen(false)}
                            style={{
                                position: 'fixed',
                                inset: 0,
                                background: 'rgba(0, 0, 0, 0.5)',
                                backdropFilter: 'blur(4px)',
                                zIndex: 190,
                            }}
                        />

                        {/* Mobile Menu Panel */}
                        <motion.div
                            initial={{ x: '100%' }}
                            animate={{ x: 0 }}
                            exit={{ x: '100%' }}
                            transition={{ type: 'spring', damping: 25, stiffness: 300 }}
                            style={{
                                position: 'fixed',
                                top: 0,
                                right: 0,
                                bottom: 0,
                                width: '280px',
                                background: 'white',
                                boxShadow: '-10px 0 40px rgba(0, 0, 0, 0.15)',
                                zIndex: 195,
                                padding: '1.5rem',
                                display: 'flex',
                                flexDirection: 'column',
                            }}
                        >
                            {/* Close Button */}
                            <div style={{
                                display: 'flex',
                                justifyContent: 'flex-end',
                                marginBottom: '1.5rem',
                            }}>
                                <motion.button
                                    whileHover={{ scale: 1.1 }}
                                    whileTap={{ scale: 0.9 }}
                                    onClick={() => setIsMobileMenuOpen(false)}
                                    style={{
                                        padding: '0.5rem',
                                        borderRadius: '8px',
                                        border: 'none',
                                        background: '#F1F5F9',
                                        color: '#475569',
                                        cursor: 'pointer',
                                    }}
                                >
                                    <X size={24} />
                                </motion.button>
                            </div>

                            {/* Mobile Nav Links */}
                            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                                {navLinks.map((link, index) => (
                                    <motion.div
                                        key={link.path}
                                        initial={{ opacity: 0, x: 20 }}
                                        animate={{ opacity: 1, x: 0 }}
                                        transition={{ delay: index * 0.05 }}
                                    >
                                        <Link
                                            to={link.path}
                                            onClick={() => setIsMobileMenuOpen(false)}
                                            style={{
                                                display: 'flex',
                                                alignItems: 'center',
                                                gap: '0.75rem',
                                                padding: '1rem',
                                                borderRadius: '12px',
                                                fontWeight: 500,
                                                fontSize: '1rem',
                                                textDecoration: 'none',
                                                transition: 'all 0.2s ease',
                                                background: isActive(link.path)
                                                    ? 'linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%)'
                                                    : 'transparent',
                                                color: isActive(link.path) ? '#3B82F6' : '#475569',
                                                border: isActive(link.path)
                                                    ? '1px solid rgba(59, 130, 246, 0.2)'
                                                    : '1px solid transparent',
                                            }}
                                        >
                                            <link.icon size={20} />
                                            {link.label}
                                        </Link>
                                    </motion.div>
                                ))}
                            </div>

                            {/* Bottom Section */}
                            <div style={{ marginTop: 'auto', paddingTop: '1.5rem', borderTop: '1px solid #E2E8F0' }}>
                                <p style={{
                                    fontSize: '0.75rem',
                                    color: '#94A3B8',
                                    textAlign: 'center',
                                }}>
                                    MedFinder © 2025
                                </p>
                            </div>
                        </motion.div>
                    </>
                )}
            </AnimatePresence>
        </>
    );
};

export default Navbar;
