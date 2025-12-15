import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Pill, TrendingDown, Search, Zap, Shield, ChevronDown,
    Building2, FlaskConical, ChevronUp, Heart, Clock,
    ArrowRight, Sparkles
} from 'lucide-react';
import SearchBar from '../components/SearchBar';
import StatsCard from '../components/StatsCard';
import { getStats } from '../api/medfinder';

/**
 * Home Page - Premium Redesign
 * 
 * Features:
 * - Full viewport hero with animated gradient
 * - Floating decorative elements
 * - Centered search bar with premium styling
 * - Collapsible stats and features sections
 * - Modern footer with centered text
 */
const Home = () => {
    const navigate = useNavigate();
    const [stats, setStats] = useState(null);
    const [showStats, setShowStats] = useState(false);
    const [showFeatures, setShowFeatures] = useState(false);

    useEffect(() => {
        loadStats();
    }, []);

    const loadStats = async () => {
        try {
            const result = await getStats();
            if (result.success) {
                setStats(result);
            }
        } catch (error) {
            console.error('Failed to load stats:', error);
        }
    };

    const handleSearch = (query) => {
        navigate(`/search?q=${encodeURIComponent(query)}`);
    };

    const handleSuggestionSelect = (suggestion) => {
        if (suggestion.type === 'composition') {
            navigate(`/formula?q=${encodeURIComponent(suggestion.value)}`);
        } else {
            navigate(`/search?q=${encodeURIComponent(suggestion.value)}`);
        }
    };

    const popularSearches = [
        'Panadol', 'Brufen', 'Paracetamol', 'Augmentin', 'Amoxil', 'Disprin'
    ];

    const features = [
        {
            icon: Search,
            title: 'Smart Search',
            description: 'Find medicines by name, brand, or chemical composition with intelligent typo tolerance',
            color: '#3B82F6',
            bgColor: 'rgba(59, 130, 246, 0.1)',
        },
        {
            icon: TrendingDown,
            title: 'Save Up to 90%',
            description: 'Discover affordable generic alternatives with the exact same composition',
            color: '#10B981',
            bgColor: 'rgba(16, 185, 129, 0.1)',
        },
        {
            icon: Zap,
            title: 'Real-time Stock',
            description: 'Check medicine availability instantly at pharmacies across Pakistan',
            color: '#F59E0B',
            bgColor: 'rgba(245, 158, 11, 0.1)',
        },
        {
            icon: Shield,
            title: 'FDA Compliant',
            description: 'Pharmaceutical equivalence checking based on FDA bioequivalence standards',
            color: '#8B5CF6',
            bgColor: 'rgba(139, 92, 246, 0.1)',
        }
    ];

    return (
        <div style={{ minHeight: '100vh' }}>
            {/* Hero Section */}
            <section style={{
                position: 'relative',
                minHeight: '100vh',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                overflow: 'hidden',
            }}>
                {/* Animated Gradient Background */}
                <div style={{
                    position: 'absolute',
                    inset: 0,
                    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f64f59 100%)',
                    backgroundSize: '200% 200%',
                    animation: 'gradientShift 8s ease infinite',
                }} />

                {/* Floating Background Elements */}
                <div style={{ position: 'absolute', inset: 0, overflow: 'hidden', pointerEvents: 'none' }}>
                    {/* Large Blurred Circle - Top Left */}
                    <motion.div
                        animate={{
                            x: [0, 50, 0],
                            y: [0, -30, 0],
                            scale: [1, 1.1, 1],
                        }}
                        transition={{ duration: 15, repeat: Infinity, ease: 'easeInOut' }}
                        style={{
                            position: 'absolute',
                            top: '10%',
                            left: '5%',
                            width: '300px',
                            height: '300px',
                            background: 'rgba(255, 255, 255, 0.1)',
                            borderRadius: '50%',
                            filter: 'blur(60px)',
                        }}
                    />

                    {/* Large Blurred Circle - Bottom Right */}
                    <motion.div
                        animate={{
                            x: [0, -40, 0],
                            y: [0, 40, 0],
                            scale: [1.2, 1, 1.2],
                        }}
                        transition={{ duration: 20, repeat: Infinity, ease: 'easeInOut' }}
                        style={{
                            position: 'absolute',
                            bottom: '10%',
                            right: '5%',
                            width: '400px',
                            height: '400px',
                            background: 'rgba(139, 92, 246, 0.3)',
                            borderRadius: '50%',
                            filter: 'blur(80px)',
                        }}
                    />

                    {/* Floating Pills */}
                    {[...Array(6)].map((_, i) => (
                        <motion.div
                            key={i}
                            animate={{
                                y: [0, -20, 0],
                                rotate: [0, 10, -10, 0],
                            }}
                            transition={{
                                duration: 4 + i,
                                repeat: Infinity,
                                delay: i * 0.5,
                                ease: 'easeInOut',
                            }}
                            style={{
                                position: 'absolute',
                                top: `${15 + (i * 12)}%`,
                                left: `${5 + (i * 15)}%`,
                                opacity: 0.1,
                            }}
                        >
                            <Pill size={30 + i * 5} color="white" />
                        </motion.div>
                    ))}
                </div>

                {/* Hero Content */}
                <div style={{
                    position: 'relative',
                    zIndex: 10,
                    maxWidth: '56rem',
                    margin: '0 auto',
                    padding: '0 1.5rem',
                    textAlign: 'center',
                }}>
                    {/* Badge */}
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.6 }}
                        style={{
                            display: 'inline-flex',
                            alignItems: 'center',
                            gap: '0.5rem',
                            padding: '0.5rem 1rem',
                            background: 'rgba(255, 255, 255, 0.15)',
                            backdropFilter: 'blur(10px)',
                            borderRadius: '9999px',
                            marginBottom: '1.5rem',
                            border: '1px solid rgba(255, 255, 255, 0.2)',
                        }}
                    >
                        <Sparkles size={16} color="white" />
                        <span style={{ color: 'white', fontSize: '0.875rem', fontWeight: 500 }}>
                            Pakistan's #1 Medicine Search Platform
                        </span>
                    </motion.div>

                    {/* Title */}
                    <motion.h1
                        initial={{ opacity: 0, y: 30 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.6, delay: 0.1 }}
                        style={{
                            fontSize: 'clamp(2.5rem, 6vw, 4.5rem)',
                            fontWeight: 800,
                            color: 'white',
                            marginBottom: '1.5rem',
                            lineHeight: 1.1,
                            fontFamily: "'Poppins', sans-serif",
                            letterSpacing: '-0.02em',
                        }}
                    >
                        Find Affordable
                        <br />
                        <span style={{
                            background: 'linear-gradient(135deg, #FCD34D 0%, #F97316 100%)',
                            WebkitBackgroundClip: 'text',
                            WebkitTextFillColor: 'transparent',
                            backgroundClip: 'text',
                        }}>
                            Medicines
                        </span>
                    </motion.h1>

                    {/* Subtitle */}
                    <motion.p
                        initial={{ opacity: 0, y: 30 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.6, delay: 0.2 }}
                        style={{
                            fontSize: 'clamp(1rem, 2vw, 1.25rem)',
                            color: 'rgba(255, 255, 255, 0.85)',
                            maxWidth: '36rem',
                            margin: '0 auto 2rem',
                            lineHeight: 1.6,
                        }}
                    >
                        Search 20,000+ medicines. Compare prices across brands.
                        Save up to 90% with generic alternatives.
                    </motion.p>

                    {/* Search Bar */}
                    <motion.div
                        initial={{ opacity: 0, y: 30 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.6, delay: 0.3 }}
                        style={{
                            maxWidth: '40rem',
                            margin: '0 auto 2rem',
                        }}
                    >
                        <SearchBar
                            onSearch={handleSearch}
                            onSuggestionSelect={handleSuggestionSelect}
                            placeholder="Search by medicine name, brand, or ingredient..."
                            size="large"
                        />
                    </motion.div>

                    {/* Popular Searches */}
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ duration: 0.6, delay: 0.5 }}
                        style={{
                            display: 'flex',
                            flexWrap: 'wrap',
                            justifyContent: 'center',
                            gap: '0.5rem',
                            alignItems: 'center',
                        }}
                    >
                        <span style={{ color: 'rgba(255, 255, 255, 0.6)', padding: '0.5rem' }}>
                            Popular:
                        </span>
                        {popularSearches.map((term, index) => (
                            <motion.button
                                key={term}
                                initial={{ opacity: 0, scale: 0.8 }}
                                animate={{ opacity: 1, scale: 1 }}
                                transition={{ delay: 0.6 + index * 0.1 }}
                                whileHover={{ scale: 1.05, background: 'rgba(255, 255, 255, 0.25)' }}
                                whileTap={{ scale: 0.95 }}
                                onClick={() => handleSearch(term)}
                                style={{
                                    padding: '0.5rem 1rem',
                                    background: 'rgba(255, 255, 255, 0.15)',
                                    backdropFilter: 'blur(10px)',
                                    borderRadius: '9999px',
                                    color: 'white',
                                    fontSize: '0.875rem',
                                    fontWeight: 500,
                                    border: '1px solid rgba(255, 255, 255, 0.2)',
                                    cursor: 'pointer',
                                    transition: 'all 0.2s ease',
                                }}
                            >
                                {term}
                            </motion.button>
                        ))}
                    </motion.div>
                </div>

                {/* Scroll Indicator */}
                <motion.div
                    animate={{ y: [0, 10, 0] }}
                    transition={{ duration: 2, repeat: Infinity }}
                    style={{
                        position: 'absolute',
                        bottom: '2rem',
                        left: '50%',
                        transform: 'translateX(-50%)',
                        color: 'rgba(255, 255, 255, 0.6)',
                    }}
                >
                    <ChevronDown size={32} />
                </motion.div>
            </section>

            {/* Actions Bar */}
            <div style={{
                maxWidth: '72rem',
                margin: '0 auto',
                padding: '2rem 1.5rem',
            }}>
                <div style={{
                    display: 'flex',
                    flexWrap: 'wrap',
                    gap: '1rem',
                    justifyContent: 'flex-start',
                }}>
                    {/* Stats Button */}
                    <motion.button
                        whileHover={{ scale: 1.02, boxShadow: '0 10px 40px -10px rgba(59, 130, 246, 0.4)' }}
                        whileTap={{ scale: 0.98 }}
                        onClick={() => setShowStats(!showStats)}
                        style={{
                            display: 'inline-flex',
                            alignItems: 'center',
                            gap: '0.75rem',
                            padding: '0.875rem 1.5rem',
                            background: 'linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%)',
                            color: 'white',
                            borderRadius: '12px',
                            fontWeight: 600,
                            fontSize: '1rem',
                            border: 'none',
                            cursor: 'pointer',
                            boxShadow: '0 4px 15px rgba(59, 130, 246, 0.3)',
                            transition: 'all 0.2s ease',
                        }}
                    >
                        <Building2 size={20} />
                        {showStats ? 'Hide Database Stats' : 'View Database Stats'}
                        {showStats ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
                    </motion.button>

                    {/* Features Button */}
                    <motion.button
                        whileHover={{ scale: 1.02, boxShadow: '0 10px 40px -10px rgba(139, 92, 246, 0.4)' }}
                        whileTap={{ scale: 0.98 }}
                        onClick={() => setShowFeatures(!showFeatures)}
                        style={{
                            display: 'inline-flex',
                            alignItems: 'center',
                            gap: '0.75rem',
                            padding: '0.875rem 1.5rem',
                            background: 'linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%)',
                            color: 'white',
                            borderRadius: '12px',
                            fontWeight: 600,
                            fontSize: '1rem',
                            border: 'none',
                            cursor: 'pointer',
                            boxShadow: '0 4px 15px rgba(139, 92, 246, 0.3)',
                            transition: 'all 0.2s ease',
                        }}
                    >
                        <Shield size={20} />
                        {showFeatures ? 'Hide Features' : 'Why Choose Us?'}
                        {showFeatures ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
                    </motion.button>

                    {/* Contact Button */}
                    <motion.button
                        whileHover={{
                            scale: 1.02,
                            borderColor: '#3B82F6',
                            color: '#3B82F6',
                        }}
                        whileTap={{ scale: 0.98 }}
                        onClick={() => navigate('/contact')}
                        style={{
                            display: 'inline-flex',
                            alignItems: 'center',
                            gap: '0.75rem',
                            padding: '0.875rem 1.5rem',
                            background: 'white',
                            color: '#475569',
                            borderRadius: '12px',
                            fontWeight: 600,
                            fontSize: '1rem',
                            border: '2px solid #E2E8F0',
                            cursor: 'pointer',
                            transition: 'all 0.2s ease',
                        }}
                    >
                        Contact Us
                        <ArrowRight size={18} />
                    </motion.button>
                </div>
            </div>

            {/* Stats Section */}
            <AnimatePresence>
                {showStats && (
                    <motion.section
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        exit={{ opacity: 0, height: 0 }}
                        transition={{ duration: 0.3 }}
                        style={{ overflow: 'hidden', background: '#F8FAFC' }}
                    >
                        <div style={{ padding: '3rem 1.5rem' }}>
                            <div style={{ maxWidth: '72rem', margin: '0 auto' }}>
                                {/* Section Header */}
                                <motion.div
                                    initial={{ opacity: 0, y: 20 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    style={{ textAlign: 'center', marginBottom: '2.5rem' }}
                                >
                                    <h2 style={{
                                        fontSize: 'clamp(1.5rem, 3vw, 2rem)',
                                        fontWeight: 700,
                                        color: '#1E293B',
                                        marginBottom: '0.75rem',
                                    }}>
                                        Powered by Data
                                    </h2>
                                    <p style={{
                                        color: '#64748B',
                                        maxWidth: '32rem',
                                        margin: '0 auto',
                                    }}>
                                        Our comprehensive database helps you make informed decisions about healthcare costs.
                                    </p>
                                </motion.div>

                                {/* Stats Grid */}
                                <div style={{
                                    display: 'grid',
                                    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                                    gap: '1.5rem',
                                }}>
                                    <StatsCard
                                        icon={Pill}
                                        value={stats?.total_medicines || 20469}
                                        label="Medicines"
                                        color="blue"
                                        delay={0}
                                    />
                                    <StatsCard
                                        icon={Building2}
                                        value={stats?.total_brands || 534}
                                        label="Brands"
                                        color="purple"
                                        delay={0.1}
                                    />
                                    <StatsCard
                                        icon={FlaskConical}
                                        value={stats?.total_compositions || 3650}
                                        label="Compositions"
                                        color="green"
                                        delay={0.2}
                                    />
                                </div>
                            </div>
                        </div>
                    </motion.section>
                )}
            </AnimatePresence>

            {/* Features Section */}
            <AnimatePresence>
                {showFeatures && (
                    <motion.section
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        exit={{ opacity: 0, height: 0 }}
                        transition={{ duration: 0.3 }}
                        style={{ overflow: 'hidden', background: 'white' }}
                    >
                        <div style={{ padding: '3rem 1.5rem' }}>
                            <div style={{ maxWidth: '72rem', margin: '0 auto' }}>
                                {/* Section Header */}
                                <motion.div
                                    initial={{ opacity: 0, y: 20 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    style={{ textAlign: 'center', marginBottom: '2.5rem' }}
                                >
                                    <h2 style={{
                                        fontSize: 'clamp(1.5rem, 3vw, 2rem)',
                                        fontWeight: 700,
                                        color: '#1E293B',
                                        marginBottom: '0.75rem',
                                    }}>
                                        Why Choose MedFinder?
                                    </h2>
                                    <p style={{
                                        color: '#64748B',
                                        maxWidth: '32rem',
                                        margin: '0 auto',
                                    }}>
                                        We make finding affordable medicine simple, safe, and fast.
                                    </p>
                                </motion.div>

                                {/* Features Grid */}
                                <div style={{
                                    display: 'grid',
                                    gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
                                    gap: '1.5rem',
                                }}>
                                    {features.map((feature, index) => (
                                        <motion.div
                                            key={feature.title}
                                            initial={{ opacity: 0, y: 20 }}
                                            animate={{ opacity: 1, y: 0 }}
                                            transition={{ delay: index * 0.1 }}
                                            whileHover={{ y: -8, boxShadow: '0 20px 40px -10px rgba(0, 0, 0, 0.1)' }}
                                            style={{
                                                padding: '1.5rem',
                                                background: '#F8FAFC',
                                                borderRadius: '16px',
                                                border: '1px solid #E2E8F0',
                                                transition: 'all 0.3s ease',
                                            }}
                                        >
                                            <div style={{
                                                display: 'inline-flex',
                                                padding: '0.75rem',
                                                background: feature.bgColor,
                                                borderRadius: '12px',
                                                marginBottom: '1rem',
                                            }}>
                                                <feature.icon size={24} color={feature.color} />
                                            </div>
                                            <h3 style={{
                                                fontSize: '1.125rem',
                                                fontWeight: 600,
                                                color: '#1E293B',
                                                marginBottom: '0.5rem',
                                            }}>
                                                {feature.title}
                                            </h3>
                                            <p style={{
                                                fontSize: '0.875rem',
                                                color: '#64748B',
                                                lineHeight: 1.6,
                                            }}>
                                                {feature.description}
                                            </p>
                                        </motion.div>
                                    ))}
                                </div>
                            </div>
                        </div>
                    </motion.section>
                )}
            </AnimatePresence>

            {/* Footer */}
            <footer style={{
                padding: '2.5rem 1.5rem',
                background: '#0F172A',
                textAlign: 'center',
            }}>
                <div style={{ maxWidth: '72rem', margin: '0 auto' }}>
                    {/* Logo */}
                    <div style={{
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        gap: '0.5rem',
                        marginBottom: '1rem',
                    }}>
                        <div style={{
                            padding: '0.5rem',
                            background: 'linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%)',
                            borderRadius: '10px',
                        }}>
                            <Pill size={20} color="white" />
                        </div>
                        <span style={{
                            color: 'white',
                            fontWeight: 600,
                            fontSize: '1.125rem',
                        }}>
                            MedFinder
                        </span>
                    </div>

                    {/* Copyright */}
                    <p style={{
                        color: '#94A3B8',
                        fontSize: '0.875rem',
                    }}>
                        © 2025 MedFinder. Database sourced from dawaai.pk. For informational purposes only.
                    </p>
                </div>
            </footer>
        </div>
    );
};

export default Home;
