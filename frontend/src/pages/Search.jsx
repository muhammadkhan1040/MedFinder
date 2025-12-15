import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { Search, ChevronDown, Package, Sparkles } from 'lucide-react';
import SearchBar from '../components/SearchBar';
import MedicineCard from '../components/MedicineCard';
import SkeletonCard from '../components/SkeletonCard';
import DetailModal from '../components/DetailModal';
import AlternativesList from '../components/AlternativesList';
import { searchByIngredient, multiFieldSearch, getSimilarMedicines, checkAvailability } from '../api/medfinder';

/**
 * Search Page - Premium Redesign
 * 
 * Features:
 * - Clean white background with subtle gradients
 * - Centered heading and search bar
 * - Category filter pills
 * - Animated results grid
 * - Smooth transitions
 */
const SearchPage = () => {
    const [searchParams, setSearchParams] = useSearchParams();
    const initialQuery = searchParams.get('q') || '';

    const [query, setQuery] = useState(initialQuery);
    const [activeTab, setActiveTab] = useState('results');
    const [results, setResults] = useState([]);
    const [alternatives, setAlternatives] = useState({ reference: null, alternatives: [] });
    const [isLoading, setIsLoading] = useState(false);
    const [isLoadingAlternatives, setIsLoadingAlternatives] = useState(false);
    const [selectedMedicine, setSelectedMedicine] = useState(null);
    const [sortBy, setSortBy] = useState('price_asc');
    const [stats, setStats] = useState({ count: 0, brand_count: 0, price_stats: {} });

    useEffect(() => {
        if (initialQuery) {
            performSearch(initialQuery);
        }
    }, [initialQuery]);

    const performSearch = async (searchQuery) => {
        if (!searchQuery.trim()) return;

        setQuery(searchQuery);
        setSearchParams({ q: searchQuery });
        setIsLoading(true);
        setResults([]);
        setActiveTab('results');

        try {
            let result = await searchByIngredient(searchQuery, 50);
            if (!result.success || result.count === 0) {
                result = await multiFieldSearch(searchQuery, 50);
            }

            if (result.success) {
                setResults(result.results || []);
                setStats({
                    count: result.count || 0,
                    brand_count: result.brand_count || 0,
                    price_stats: result.price_stats || {}
                });
            }
        } catch (error) {
            console.error('Search failed:', error);
        } finally {
            setIsLoading(false);
        }
    };

    const loadAlternatives = async (medicine) => {
        if (!medicine?.name) return;
        setIsLoadingAlternatives(true);
        try {
            const result = await getSimilarMedicines(medicine.name, 10);
            if (result.success) {
                setAlternatives({
                    reference: result.reference_medicine,
                    alternatives: result.alternatives || []
                });
            }
        } catch (error) {
            console.error('Failed to load alternatives:', error);
        } finally {
            setIsLoadingAlternatives(false);
        }
    };

    const handleSearch = (searchQuery) => {
        performSearch(searchQuery);
    };

    const handleCheckStock = async (medicine) => {
        try {
            const result = await checkAvailability(medicine.name);
            return result.available;
        } catch (error) {
            console.error('Availability check failed:', error);
            return null;
        }
    };

    const handleFindAlternatives = (medicine) => {
        setActiveTab('alternatives');
        window.scrollTo({ top: 300, behavior: 'smooth' });
        loadAlternatives(medicine);
    };

    const sortedResults = [...results].sort((a, b) => {
        const priceA = parseFloat((a.price || '0').replace(/[^0-9.]/g, '')) || 0;
        const priceB = parseFloat((b.price || '0').replace(/[^0-9.]/g, '')) || 0;

        switch (sortBy) {
            case 'price_asc': return priceA - priceB;
            case 'price_desc': return priceB - priceA;
            case 'name_asc': return (a.name || '').localeCompare(b.name || '');
            default: return 0;
        }
    });

    const categories = [
        "Pain Relief", "Antibiotics", "Vitamins", "Cardiovascular",
        "Diabetes", "Allergies", "Supplements"
    ];

    return (
        <div style={{ minHeight: '100vh', background: '#FAFBFC', paddingTop: '5rem' }}>
            {/* Header Section */}
            <header style={{
                padding: '3rem 1.5rem 2rem',
                background: 'linear-gradient(180deg, white 0%, #FAFBFC 100%)',
                borderBottom: '1px solid #E2E8F0',
            }}>
                <div style={{ maxWidth: '72rem', margin: '0 auto', textAlign: 'center' }}>
                    {/* Title */}
                    <motion.h1
                        initial={{ opacity: 0, y: -20 }}
                        animate={{ opacity: 1, y: 0 }}
                        style={{
                            fontSize: 'clamp(2rem, 4vw, 3rem)',
                            fontWeight: 700,
                            color: '#0F172A',
                            marginBottom: '1rem',
                            fontFamily: "'Poppins', sans-serif",
                            letterSpacing: '-0.02em',
                        }}
                    >
                        Find Your Medicine
                    </motion.h1>

                    <motion.p
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ delay: 0.1 }}
                        style={{
                            color: '#64748B',
                            marginBottom: '2rem',
                            fontSize: '1.0625rem',
                        }}
                    >
                        Search by name, brand, or chemical formula
                    </motion.p>

                    {/* Search Bar */}
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.2 }}
                        style={{ maxWidth: '40rem', margin: '0 auto 2rem' }}
                    >
                        <SearchBar
                            onSearch={handleSearch}
                            onSuggestionSelect={(s) => performSearch(s.value)}
                            placeholder="Search by name, brand, or formula..."
                        />
                    </motion.div>

                    {/* Category Pills */}
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ delay: 0.3 }}
                        style={{
                            display: 'flex',
                            flexWrap: 'wrap',
                            justifyContent: 'center',
                            gap: '0.5rem',
                        }}
                    >
                        {categories.map((cat, index) => (
                            <motion.button
                                key={cat}
                                whileHover={{ scale: 1.05, background: '#3B82F6', color: 'white' }}
                                whileTap={{ scale: 0.95 }}
                                onClick={() => performSearch(cat)}
                                style={{
                                    padding: '0.5rem 1rem',
                                    background: 'white',
                                    color: '#475569',
                                    border: '1px solid #E2E8F0',
                                    borderRadius: '9999px',
                                    fontSize: '0.875rem',
                                    fontWeight: 500,
                                    cursor: 'pointer',
                                    transition: 'all 0.2s ease',
                                }}
                            >
                                {cat}
                            </motion.button>
                        ))}
                    </motion.div>
                </div>
            </header>

            {/* Main Content */}
            <main style={{ maxWidth: '80rem', margin: '0 auto', padding: '2rem 1.5rem' }}>
                {/* Results Header */}
                {(query || activeTab === 'alternatives') && (
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        style={{
                            display: 'flex',
                            flexWrap: 'wrap',
                            alignItems: 'center',
                            justifyContent: 'space-between',
                            gap: '1rem',
                            marginBottom: '2rem',
                            padding: '1.25rem 1.5rem',
                            background: 'white',
                            borderRadius: '16px',
                            boxShadow: '0 1px 3px rgba(0, 0, 0, 0.05)',
                            border: '1px solid #E2E8F0',
                        }}
                    >
                        <div>
                            {activeTab === 'results' ? (
                                <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                                    <div style={{
                                        padding: '0.5rem',
                                        background: 'linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%)',
                                        borderRadius: '10px',
                                    }}>
                                        <Package size={20} style={{ color: '#3B82F6' }} />
                                    </div>
                                    <div>
                                        <h2 style={{
                                            fontSize: '1.125rem',
                                            fontWeight: 600,
                                            color: '#0F172A',
                                            margin: 0,
                                        }}>
                                            {results.length > 0 ? (
                                                <>
                                                    <span style={{ color: '#3B82F6' }}>{results.length}</span> results for "{query}"
                                                </>
                                            ) : isLoading ? (
                                                'Searching...'
                                            ) : (
                                                `No results for "${query}"`
                                            )}
                                        </h2>
                                        {stats.count > 0 && !isLoading && (
                                            <p style={{
                                                fontSize: '0.8125rem',
                                                color: '#64748B',
                                                margin: 0,
                                            }}>
                                                {stats.brand_count} brands • Price range: Rs. {stats.price_stats.min?.toFixed(0) || '0'} - Rs. {stats.price_stats.max?.toFixed(0) || '0'}
                                            </p>
                                        )}
                                    </div>
                                </div>
                            ) : (
                                <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                                    <div style={{
                                        padding: '0.5rem',
                                        background: 'linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(236, 72, 153, 0.1) 100%)',
                                        borderRadius: '10px',
                                    }}>
                                        <Sparkles size={20} style={{ color: '#8B5CF6' }} />
                                    </div>
                                    <h2 style={{
                                        fontSize: '1.125rem',
                                        fontWeight: 600,
                                        color: '#0F172A',
                                        margin: 0,
                                    }}>
                                        Alternatives for "{alternatives.reference?.name}"
                                    </h2>
                                </div>
                            )}
                        </div>

                        {/* Sort Dropdown */}
                        <div style={{
                            display: 'flex',
                            alignItems: 'center',
                            gap: '0.5rem',
                        }}>
                            <span style={{ fontSize: '0.875rem', color: '#64748B' }}>Sort by:</span>
                            <div style={{ position: 'relative' }}>
                                <select
                                    value={sortBy}
                                    onChange={(e) => setSortBy(e.target.value)}
                                    style={{
                                        appearance: 'none',
                                        padding: '0.5rem 2rem 0.5rem 0.75rem',
                                        background: '#F8FAFC',
                                        border: '1px solid #E2E8F0',
                                        borderRadius: '8px',
                                        fontSize: '0.875rem',
                                        fontWeight: 500,
                                        color: '#0F172A',
                                        cursor: 'pointer',
                                        outline: 'none',
                                    }}
                                >
                                    <option value="price_asc">Price: Low to High</option>
                                    <option value="price_desc">Price: High to Low</option>
                                    <option value="name_asc">Name: A to Z</option>
                                </select>
                                <ChevronDown
                                    size={14}
                                    style={{
                                        position: 'absolute',
                                        right: '0.75rem',
                                        top: '50%',
                                        transform: 'translateY(-50%)',
                                        pointerEvents: 'none',
                                        color: '#64748B',
                                    }}
                                />
                            </div>
                        </div>
                    </motion.div>
                )}

                {/* Loading State */}
                <AnimatePresence>
                    {isLoading && (
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            style={{
                                display: 'grid',
                                gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
                                gap: '1.5rem',
                            }}
                        >
                            {[...Array(8)].map((_, i) => (
                                <SkeletonCard key={i} />
                            ))}
                        </motion.div>
                    )}
                </AnimatePresence>

                {/* Results Grid */}
                {!isLoading && activeTab === 'results' && sortedResults.length > 0 && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        style={{
                            display: 'grid',
                            gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
                            gap: '1.5rem',
                        }}
                    >
                        {sortedResults.map((medicine, index) => (
                            <MedicineCard
                                key={medicine.name + index}
                                medicine={medicine}
                                onViewDetails={(m) => setSelectedMedicine(m)}
                                onCheckStock={handleCheckStock}
                                onCompare={() => handleFindAlternatives(medicine)}
                                index={index}
                            />
                        ))}
                    </motion.div>
                )}

                {/* Alternatives View */}
                {activeTab === 'alternatives' && !isLoadingAlternatives && alternatives.reference && (
                    <AlternativesList
                        referenceMedicine={alternatives.reference}
                        alternatives={alternatives.alternatives}
                        onViewDetails={(m) => setSelectedMedicine(m)}
                        onCheckStock={handleCheckStock}
                        onSelectAlternative={(alt) => setSelectedMedicine(alt)}
                    />
                )}

                {/* Empty State */}
                {!query && !isLoading && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        style={{
                            textAlign: 'center',
                            padding: '4rem 1rem',
                        }}
                    >
                        <div style={{
                            display: 'inline-flex',
                            padding: '1.5rem',
                            background: 'linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%)',
                            borderRadius: '20px',
                            marginBottom: '1.5rem',
                        }}>
                            <Search size={48} style={{ color: '#3B82F6' }} />
                        </div>
                        <h2 style={{
                            fontSize: '1.5rem',
                            fontWeight: 600,
                            color: '#0F172A',
                            marginBottom: '0.5rem',
                        }}>
                            Start Your Search
                        </h2>
                        <p style={{ color: '#64748B', maxWidth: '24rem', margin: '0 auto' }}>
                            Use the search bar above to find medicines by name, brand, or chemical formula.
                        </p>
                    </motion.div>
                )}

                {/* No Results State */}
                {!isLoading && query && results.length === 0 && activeTab === 'results' && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        style={{
                            textAlign: 'center',
                            padding: '4rem 1rem',
                        }}
                    >
                        <div style={{
                            display: 'inline-flex',
                            padding: '1.5rem',
                            background: 'rgba(239, 68, 68, 0.1)',
                            borderRadius: '20px',
                            marginBottom: '1.5rem',
                        }}>
                            <Package size={48} style={{ color: '#EF4444' }} />
                        </div>
                        <h2 style={{
                            fontSize: '1.5rem',
                            fontWeight: 600,
                            color: '#0F172A',
                            marginBottom: '0.5rem',
                        }}>
                            No Results Found
                        </h2>
                        <p style={{ color: '#64748B', maxWidth: '24rem', margin: '0 auto' }}>
                            We couldn't find any medicines matching "{query}". Try a different search term.
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

export default SearchPage;
