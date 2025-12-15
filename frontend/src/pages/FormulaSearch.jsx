import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { FlaskConical, Search, Filter, X, BarChart3, Building2, Pill, Sparkles } from 'lucide-react';
import { searchByComposition, getAvailableDosages } from '../api/medfinder';
import MedicineCard from '../components/MedicineCard';
import SkeletonCard from '../components/SkeletonCard';
import DetailModal from '../components/DetailModal';
import { checkAvailability } from '../api/medfinder';

/**
 * Formula Search Page - Premium Redesign
 * 
 * Features:
 * - Gradient hero header
 * - Search by chemical formula/composition
 * - Animated dosage filter chips
 * - Stats bar with glassmorphism
 * - Consistent styling with other pages
 */
const FormulaSearch = () => {
    const [searchParams, setSearchParams] = useSearchParams();
    const initialQuery = searchParams.get('q') || '';

    const [query, setQuery] = useState(initialQuery);
    const [results, setResults] = useState([]);
    const [availableDosages, setAvailableDosages] = useState([]);
    const [selectedDosage, setSelectedDosage] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [selectedMedicine, setSelectedMedicine] = useState(null);
    const [stats, setStats] = useState({ count: 0, price_stats: {} });

    useEffect(() => {
        if (initialQuery) {
            performSearch(initialQuery);
        }
    }, [initialQuery]);

    const performSearch = async (formula, dosageFilter = null) => {
        if (!formula.trim()) return;

        setQuery(formula);
        setSearchParams({ q: formula });
        setIsLoading(true);

        try {
            const result = await searchByComposition(formula, dosageFilter, 100);

            if (result.success) {
                setResults(result.results || []);
                setAvailableDosages(result.available_dosages || []);
                setStats({
                    count: result.count || 0,
                    price_stats: result.price_stats || {}
                });
            }
        } catch (error) {
            console.error('Search failed:', error);
        } finally {
            setIsLoading(false);
        }
    };

    const handleSearchSubmit = (e) => {
        e.preventDefault();
        setSelectedDosage(null);
        performSearch(query);
    };

    const handleDosageFilter = (dosage) => {
        if (selectedDosage === dosage) {
            setSelectedDosage(null);
            performSearch(query);
        } else {
            setSelectedDosage(dosage);
            performSearch(query, dosage);
        }
    };

    const handleViewDetails = (medicine) => {
        setSelectedMedicine(medicine);
    };

    const handleCheckStock = async (medicine) => {
        try {
            const result = await checkAvailability(medicine.name);
            return result.available;
        } catch (error) {
            return null;
        }
    };

    // Group results by brand
    const brandGroups = results.reduce((acc, med) => {
        const brand = med.brand || 'Unknown';
        if (!acc[brand]) acc[brand] = [];
        acc[brand].push(med);
        return acc;
    }, {});

    const popularFormulas = [
        'Paracetamol', 'Ibuprofen', 'Amoxicillin', 'Omeprazole',
        'Diclofenac', 'Metformin', 'Ciprofloxacin'
    ];

    return (
        <div style={{ minHeight: '100vh', background: '#FAFBFC', paddingTop: '4rem' }}>
            {/* Hero Header */}
            <header style={{
                position: 'relative',
                background: 'linear-gradient(135deg, #8B5CF6 0%, #6D28D9 50%, #4C1D95 100%)',
                overflow: 'hidden',
            }}>
                {/* Background Shapes */}
                <div style={{ position: 'absolute', inset: 0, overflow: 'hidden', pointerEvents: 'none' }}>
                    <motion.div
                        animate={{ x: [0, 30, 0], y: [0, -20, 0] }}
                        transition={{ duration: 8, repeat: Infinity }}
                        style={{
                            position: 'absolute',
                            top: '20%',
                            left: '10%',
                            width: '200px',
                            height: '200px',
                            background: 'rgba(255, 255, 255, 0.1)',
                            borderRadius: '50%',
                            filter: 'blur(40px)',
                        }}
                    />
                    <motion.div
                        animate={{ x: [0, -20, 0], y: [0, 30, 0] }}
                        transition={{ duration: 10, repeat: Infinity }}
                        style={{
                            position: 'absolute',
                            bottom: '10%',
                            right: '15%',
                            width: '300px',
                            height: '300px',
                            background: 'rgba(236, 72, 153, 0.2)',
                            borderRadius: '50%',
                            filter: 'blur(60px)',
                        }}
                    />
                </div>

                {/* Content */}
                <div style={{
                    position: 'relative',
                    zIndex: 10,
                    maxWidth: '56rem',
                    margin: '0 auto',
                    padding: '4rem 1.5rem',
                    textAlign: 'center',
                }}>
                    {/* Badge */}
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
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
                        <FlaskConical size={18} color="white" />
                        <span style={{ color: 'white', fontSize: '0.875rem', fontWeight: 500 }}>
                            Formula-Based Search
                        </span>
                    </motion.div>

                    {/* Title */}
                    <motion.h1
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.1 }}
                        style={{
                            fontSize: 'clamp(1.75rem, 4vw, 2.75rem)',
                            fontWeight: 700,
                            color: 'white',
                            marginBottom: '1rem',
                            fontFamily: "'Poppins', sans-serif",
                        }}
                    >
                        Search by Chemical Composition
                    </motion.h1>

                    <motion.p
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ delay: 0.2 }}
                        style={{
                            color: 'rgba(255, 255, 255, 0.85)',
                            marginBottom: '2rem',
                            fontSize: '1.0625rem',
                        }}
                    >
                        Enter an active ingredient to find all medicines containing it
                    </motion.p>

                    {/* Search Form */}
                    <motion.form
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.3 }}
                        onSubmit={handleSearchSubmit}
                        style={{ maxWidth: '36rem', margin: '0 auto' }}
                    >
                        <div style={{
                            position: 'relative',
                            background: 'white',
                            borderRadius: '16px',
                            boxShadow: '0 20px 40px -10px rgba(0, 0, 0, 0.2)',
                        }}>
                            <FlaskConical
                                size={20}
                                style={{
                                    position: 'absolute',
                                    left: '1.25rem',
                                    top: '50%',
                                    transform: 'translateY(-50%)',
                                    color: '#8B5CF6',
                                }}
                            />
                            <input
                                type="text"
                                value={query}
                                onChange={(e) => setQuery(e.target.value)}
                                placeholder="e.g., Paracetamol, Ibuprofen, Amoxicillin..."
                                style={{
                                    width: '100%',
                                    padding: '1.125rem 7rem 1.125rem 3.5rem',
                                    fontSize: '1rem',
                                    border: 'none',
                                    borderRadius: '16px',
                                    outline: 'none',
                                    color: '#0F172A',
                                }}
                            />
                            <button
                                type="submit"
                                style={{
                                    position: 'absolute',
                                    right: '0.5rem',
                                    top: '50%',
                                    transform: 'translateY(-50%)',
                                    padding: '0.625rem 1.25rem',
                                    background: 'linear-gradient(135deg, #8B5CF6 0%, #6D28D9 100%)',
                                    color: 'white',
                                    border: 'none',
                                    borderRadius: '12px',
                                    fontWeight: 600,
                                    cursor: 'pointer',
                                    display: 'flex',
                                    alignItems: 'center',
                                    gap: '0.5rem',
                                    boxShadow: '0 4px 15px rgba(139, 92, 246, 0.3)',
                                }}
                            >
                                <Search size={18} />
                                Search
                            </button>
                        </div>
                    </motion.form>

                    {/* Popular Formulas */}
                    {!query && (
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            transition={{ delay: 0.4 }}
                            style={{
                                marginTop: '1.5rem',
                                display: 'flex',
                                flexWrap: 'wrap',
                                justifyContent: 'center',
                                gap: '0.5rem',
                            }}
                        >
                            <span style={{ color: 'rgba(255, 255, 255, 0.6)', padding: '0.5rem' }}>
                                Popular:
                            </span>
                            {popularFormulas.map((formula) => (
                                <motion.button
                                    key={formula}
                                    whileHover={{ scale: 1.05, background: 'rgba(255, 255, 255, 0.25)' }}
                                    whileTap={{ scale: 0.95 }}
                                    onClick={() => performSearch(formula)}
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
                                    {formula}
                                </motion.button>
                            ))}
                        </motion.div>
                    )}
                </div>
            </header>

            {/* Main Content */}
            <main style={{ maxWidth: '80rem', margin: '0 auto', padding: '2rem 1.5rem' }}>
                {/* Stats Bar */}
                <AnimatePresence>
                    {stats.count > 0 && !isLoading && (
                        <motion.div
                            initial={{ opacity: 0, y: -20 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -20 }}
                            style={{
                                background: 'white',
                                borderRadius: '16px',
                                padding: '1.5rem',
                                marginBottom: '2rem',
                                boxShadow: '0 1px 3px rgba(0, 0, 0, 0.05)',
                                border: '1px solid #E2E8F0',
                            }}
                        >
                            <div style={{
                                display: 'grid',
                                gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
                                gap: '1.5rem',
                                textAlign: 'center',
                            }}>
                                <div>
                                    <p style={{ color: '#94A3B8', fontSize: '0.75rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.25rem' }}>
                                        Formula
                                    </p>
                                    <p style={{
                                        fontSize: '1.25rem',
                                        fontWeight: 700,
                                        background: 'linear-gradient(135deg, #8B5CF6 0%, #6D28D9 100%)',
                                        WebkitBackgroundClip: 'text',
                                        WebkitTextFillColor: 'transparent',
                                        backgroundClip: 'text',
                                    }}>
                                        {query}
                                    </p>
                                </div>
                                <div>
                                    <p style={{ color: '#94A3B8', fontSize: '0.75rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.25rem' }}>
                                        Medicines Found
                                    </p>
                                    <p style={{ fontSize: '1.25rem', fontWeight: 700, color: '#0F172A' }}>
                                        {stats.count}
                                    </p>
                                </div>
                                <div>
                                    <p style={{ color: '#94A3B8', fontSize: '0.75rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.25rem' }}>
                                        Price Range
                                    </p>
                                    <p style={{ fontSize: '1.25rem', fontWeight: 700, color: '#0F172A', fontFamily: "'JetBrains Mono', monospace" }}>
                                        Rs. {stats.price_stats.min?.toFixed(0) || '0'} - {stats.price_stats.max?.toFixed(0) || '0'}
                                    </p>
                                </div>
                                <div>
                                    <p style={{ color: '#94A3B8', fontSize: '0.75rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.25rem' }}>
                                        Brands
                                    </p>
                                    <p style={{ fontSize: '1.25rem', fontWeight: 700, color: '#0F172A' }}>
                                        {Object.keys(brandGroups).length}
                                    </p>
                                </div>
                            </div>
                        </motion.div>
                    )}
                </AnimatePresence>

                {/* Dosage Filters */}
                {availableDosages.length > 0 && !isLoading && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        style={{ marginBottom: '2rem' }}
                    >
                        <div style={{
                            display: 'flex',
                            alignItems: 'center',
                            gap: '0.75rem',
                            marginBottom: '1rem',
                        }}>
                            <Filter size={18} style={{ color: '#64748B' }} />
                            <span style={{ fontWeight: 600, color: '#475569' }}>Filter by Dosage:</span>
                            {selectedDosage && (
                                <button
                                    onClick={() => handleDosageFilter(selectedDosage)}
                                    style={{
                                        fontSize: '0.8125rem',
                                        color: '#EF4444',
                                        background: 'none',
                                        border: 'none',
                                        cursor: 'pointer',
                                        fontWeight: 500,
                                    }}
                                >
                                    Clear filter
                                </button>
                            )}
                        </div>
                        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                            {availableDosages.slice(0, 12).map((dosage) => (
                                <motion.button
                                    key={dosage}
                                    whileHover={{ scale: 1.02 }}
                                    whileTap={{ scale: 0.98 }}
                                    onClick={() => handleDosageFilter(dosage)}
                                    style={{
                                        padding: '0.5rem 1rem',
                                        borderRadius: '9999px',
                                        fontWeight: 500,
                                        fontSize: '0.875rem',
                                        cursor: 'pointer',
                                        transition: 'all 0.2s ease',
                                        background: selectedDosage === dosage
                                            ? 'linear-gradient(135deg, #8B5CF6 0%, #6D28D9 100%)'
                                            : 'white',
                                        color: selectedDosage === dosage ? 'white' : '#475569',
                                        border: selectedDosage === dosage
                                            ? 'none'
                                            : '1px solid #E2E8F0',
                                        boxShadow: selectedDosage === dosage
                                            ? '0 4px 15px rgba(139, 92, 246, 0.3)'
                                            : 'none',
                                    }}
                                >
                                    {dosage}
                                </motion.button>
                            ))}
                            {availableDosages.length > 12 && (
                                <span style={{
                                    padding: '0.5rem 1rem',
                                    color: '#94A3B8',
                                    fontSize: '0.875rem',
                                }}>
                                    +{availableDosages.length - 12} more
                                </span>
                            )}
                        </div>
                    </motion.div>
                )}

                {/* Loading State */}
                {isLoading && (
                    <div style={{
                        display: 'grid',
                        gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
                        gap: '1.5rem',
                    }}>
                        {[...Array(6)].map((_, i) => (
                            <SkeletonCard key={i} />
                        ))}
                    </div>
                )}

                {/* Results Grid */}
                {!isLoading && results.length > 0 && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        style={{
                            display: 'grid',
                            gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
                            gap: '1.5rem',
                        }}
                    >
                        {results.map((medicine, index) => (
                            <MedicineCard
                                key={medicine.name + index}
                                medicine={medicine}
                                onViewDetails={handleViewDetails}
                                onCheckStock={handleCheckStock}
                                index={index}
                            />
                        ))}
                    </motion.div>
                )}

                {/* No Results */}
                {!isLoading && query && results.length === 0 && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        style={{ textAlign: 'center', padding: '4rem 1rem' }}
                    >
                        <div style={{
                            display: 'inline-flex',
                            padding: '1.5rem',
                            background: 'rgba(239, 68, 68, 0.1)',
                            borderRadius: '20px',
                            marginBottom: '1.5rem',
                        }}>
                            <FlaskConical size={48} style={{ color: '#EF4444' }} />
                        </div>
                        <h2 style={{
                            fontSize: '1.5rem',
                            fontWeight: 600,
                            color: '#0F172A',
                            marginBottom: '0.5rem',
                        }}>
                            No medicines found with "{query}"
                        </h2>
                        <p style={{ color: '#64748B' }}>
                            Try a different formula or check your spelling.
                        </p>
                    </motion.div>
                )}

                {/* Initial State */}
                {!isLoading && !query && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        style={{ textAlign: 'center', padding: '4rem 1rem' }}
                    >
                        <div style={{
                            display: 'inline-flex',
                            padding: '1.5rem',
                            background: 'linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(109, 40, 217, 0.1) 100%)',
                            borderRadius: '20px',
                            marginBottom: '1.5rem',
                        }}>
                            <FlaskConical size={48} style={{ color: '#8B5CF6' }} />
                        </div>
                        <h2 style={{
                            fontSize: '1.5rem',
                            fontWeight: 600,
                            color: '#0F172A',
                            marginBottom: '0.5rem',
                        }}>
                            Search by Active Ingredient
                        </h2>
                        <p style={{ color: '#64748B', maxWidth: '28rem', margin: '0 auto' }}>
                            Enter a chemical formula like "Paracetamol" or "Ibuprofen" to find all medicines containing it.
                        </p>
                    </motion.div>
                )}
            </main>

            {/* Detail Modal */}
            <DetailModal
                medicine={selectedMedicine}
                isOpen={!!selectedMedicine}
                onClose={() => setSelectedMedicine(null)}
            />
        </div>
    );
};

export default FormulaSearch;
