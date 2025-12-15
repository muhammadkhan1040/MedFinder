import { useState } from 'react';
import { motion } from 'framer-motion';
import { Sparkles, Activity, Search, Loader2, AlertCircle, Brain, Zap, DollarSign } from 'lucide-react';
import SymptomSearchResults from '../components/SymptomSearchResults';

/**
 * SymptomSearch Page - Premium Redesign
 * 
 * AI-powered symptom analysis with inline styles
 */
const SymptomSearch = () => {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleSearch = async () => {
        if (!query.trim() || query.trim().length < 5) {
            setError('Please provide more detail about your symptoms');
            return;
        }

        setIsLoading(true);
        setError(null);
        setResults(null);

        try {
            const response = await fetch('http://localhost:5000/api/symptom-search', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ symptoms: query, max_results: 10 }),
            });

            const data = await response.json();

            if (!data.success) {
                throw new Error(data.error || 'Failed to analyze symptoms');
            }

            setResults(data);
        } catch (err) {
            console.error('Search error:', err);
            setError(err.message || 'Something went wrong. Please try again.');
        } finally {
            setIsLoading(false);
        }
    };

    const exampleQueries = [
        "Severe headache with sensitivity to light",
        "High fever with body aches and chills",
        "Stomach pain and nausea after eating",
        "Persistent cough with chest congestion"
    ];

    return (
        <div style={{ minHeight: '100vh', background: '#FAFBFC', paddingTop: '4rem' }}>
            {/* Hero Section */}
            <section style={{
                position: 'relative',
                background: 'linear-gradient(135deg, #1E3A8A 0%, #3730A3 50%, #5B21B6 100%)',
                overflow: 'hidden',
                paddingBottom: '6rem',
            }}>
                {/* Animated Background */}
                <div style={{ position: 'absolute', inset: 0, overflow: 'hidden', pointerEvents: 'none' }}>
                    <motion.div
                        animate={{ x: [0, 30, 0], y: [0, -20, 0] }}
                        transition={{ duration: 10, repeat: Infinity }}
                        style={{
                            position: 'absolute',
                            top: '10%',
                            left: '5%',
                            width: '300px',
                            height: '300px',
                            background: 'rgba(59, 130, 246, 0.2)',
                            borderRadius: '50%',
                            filter: 'blur(60px)',
                        }}
                    />
                    <motion.div
                        animate={{ x: [0, -20, 0], y: [0, 30, 0] }}
                        transition={{ duration: 12, repeat: Infinity }}
                        style={{
                            position: 'absolute',
                            bottom: '10%',
                            right: '10%',
                            width: '400px',
                            height: '400px',
                            background: 'rgba(139, 92, 246, 0.2)',
                            borderRadius: '50%',
                            filter: 'blur(80px)',
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
                            background: 'rgba(255, 255, 255, 0.1)',
                            backdropFilter: 'blur(10px)',
                            borderRadius: '9999px',
                            marginBottom: '1.5rem',
                            border: '1px solid rgba(255, 255, 255, 0.2)',
                        }}
                    >
                        <Sparkles size={16} style={{ color: '#FCD34D' }} />
                        <span style={{ color: 'white', fontSize: '0.875rem', fontWeight: 500 }}>
                            AI-Powered Medical Assistant
                        </span>
                    </motion.div>

                    {/* Title */}
                    <motion.h1
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.1 }}
                        style={{
                            fontSize: 'clamp(2rem, 5vw, 3.5rem)',
                            fontWeight: 800,
                            color: 'white',
                            marginBottom: '1rem',
                            fontFamily: "'Poppins', sans-serif",
                            lineHeight: 1.2,
                        }}
                    >
                        Smart Symptom{' '}
                        <span style={{
                            background: 'linear-gradient(135deg, #93C5FD 0%, #C4B5FD 100%)',
                            WebkitBackgroundClip: 'text',
                            WebkitTextFillColor: 'transparent',
                            backgroundClip: 'text',
                        }}>
                            Analysis
                        </span>
                    </motion.h1>

                    <motion.p
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ delay: 0.2 }}
                        style={{
                            color: 'rgba(255, 255, 255, 0.85)',
                            fontSize: '1.125rem',
                            maxWidth: '40rem',
                            margin: '0 auto 2.5rem',
                            lineHeight: 1.6,
                        }}
                    >
                        Describe your symptoms and our AI will analyze medical databases to recommend
                        appropriate treatments with the best prices.
                    </motion.p>

                    {/* Search Box */}
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.3 }}
                        style={{
                            maxWidth: '42rem',
                            margin: '0 auto',
                        }}
                    >
                        <div style={{
                            background: 'white',
                            borderRadius: '20px',
                            boxShadow: '0 25px 60px -15px rgba(0, 0, 0, 0.3)',
                            overflow: 'hidden',
                        }}>
                            <textarea
                                value={query}
                                onChange={(e) => {
                                    setQuery(e.target.value);
                                    if (error) setError(null);
                                }}
                                placeholder="Describe your symptoms in detail..."
                                disabled={isLoading}
                                style={{
                                    width: '100%',
                                    padding: '1.5rem',
                                    border: 'none',
                                    outline: 'none',
                                    resize: 'none',
                                    minHeight: '120px',
                                    fontSize: '1rem',
                                    color: '#1F2937',
                                    fontFamily: 'inherit',
                                    background: 'transparent',
                                }}
                            />
                            <div style={{
                                display: 'flex',
                                justifyContent: 'space-between',
                                alignItems: 'center',
                                padding: '0.75rem 1.5rem',
                                borderTop: '1px solid #E5E7EB',
                                background: '#F9FAFB',
                            }}>
                                <span style={{
                                    fontSize: '0.75rem',
                                    color: query.length > 500 ? '#EF4444' : '#9CA3AF',
                                }}>
                                    {query.length}/500 characters
                                </span>
                                <motion.button
                                    whileHover={{ scale: 1.02 }}
                                    whileTap={{ scale: 0.98 }}
                                    onClick={handleSearch}
                                    disabled={isLoading || !query.trim()}
                                    style={{
                                        padding: '0.75rem 1.5rem',
                                        background: isLoading || !query.trim()
                                            ? '#D1D5DB'
                                            : 'linear-gradient(135deg, #3B82F6 0%, #6366F1 100%)',
                                        color: 'white',
                                        border: 'none',
                                        borderRadius: '12px',
                                        fontWeight: 600,
                                        fontSize: '0.9375rem',
                                        cursor: isLoading || !query.trim() ? 'not-allowed' : 'pointer',
                                        display: 'flex',
                                        alignItems: 'center',
                                        gap: '0.5rem',
                                        boxShadow: isLoading || !query.trim() ? 'none' : '0 4px 15px rgba(59, 130, 246, 0.3)',
                                    }}
                                >
                                    {isLoading ? (
                                        <><Loader2 size={18} style={{ animation: 'spin 1s linear infinite' }} /> Analyzing...</>
                                    ) : (
                                        <><Search size={18} /> Analyze Symptoms</>
                                    )}
                                </motion.button>
                            </div>
                        </div>

                        {/* Error Message */}
                        {error && (
                            <motion.div
                                initial={{ opacity: 0, y: -10 }}
                                animate={{ opacity: 1, y: 0 }}
                                style={{
                                    display: 'flex',
                                    alignItems: 'center',
                                    gap: '0.5rem',
                                    marginTop: '1rem',
                                    padding: '0.75rem 1rem',
                                    background: 'rgba(239, 68, 68, 0.1)',
                                    border: '1px solid rgba(239, 68, 68, 0.3)',
                                    borderRadius: '10px',
                                    color: '#FCA5A5',
                                    fontSize: '0.875rem',
                                }}
                            >
                                <AlertCircle size={16} />
                                {error}
                            </motion.div>
                        )}

                        {/* Example Queries */}
                        <div style={{ marginTop: '1.5rem' }}>
                            <span style={{ color: 'rgba(255, 255, 255, 0.6)', fontSize: '0.875rem' }}>Try: </span>
                            <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: '0.5rem', marginTop: '0.5rem' }}>
                                {exampleQueries.map((ex, i) => (
                                    <button
                                        key={i}
                                        onClick={() => setQuery(ex)}
                                        style={{
                                            padding: '0.375rem 0.875rem',
                                            background: 'rgba(255, 255, 255, 0.1)',
                                            border: '1px solid rgba(255, 255, 255, 0.2)',
                                            borderRadius: '9999px',
                                            color: 'rgba(255, 255, 255, 0.9)',
                                            fontSize: '0.8125rem',
                                            cursor: 'pointer',
                                            transition: 'all 0.2s ease',
                                        }}
                                        onMouseEnter={(e) => e.currentTarget.style.background = 'rgba(255, 255, 255, 0.2)'}
                                        onMouseLeave={(e) => e.currentTarget.style.background = 'rgba(255, 255, 255, 0.1)'}
                                    >
                                        "{ex.slice(0, 25)}..."
                                    </button>
                                ))}
                            </div>
                        </div>
                    </motion.div>
                </div>
            </section>

            {/* Results Section */}
            <main style={{ maxWidth: '72rem', margin: '0 auto', padding: '3rem 1.5rem' }}>
                {results ? (
                    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                        <SymptomSearchResults results={results} />
                    </motion.div>
                ) : !isLoading && (
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        style={{
                            display: 'grid',
                            gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
                            gap: '1.5rem',
                            marginTop: '-2rem',
                        }}
                    >
                        {/* Feature Cards */}
                        {[
                            { icon: Brain, color: '#3B82F6', title: 'AI Analysis', desc: 'Advanced symptom recognition and medical context understanding' },
                            { icon: Zap, color: '#8B5CF6', title: 'Smart Matching', desc: 'Matches symptoms to medicines using RAG technology' },
                            { icon: DollarSign, color: '#10B981', title: 'Best Prices', desc: 'Finds all brands and alternatives to help you save money' },
                        ].map((feature, i) => (
                            <motion.div
                                key={i}
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: i * 0.1 }}
                                style={{
                                    padding: '1.5rem',
                                    background: 'white',
                                    borderRadius: '16px',
                                    boxShadow: '0 4px 20px -5px rgba(0, 0, 0, 0.08)',
                                    border: '1px solid #E5E7EB',
                                    textAlign: 'center',
                                }}
                            >
                                <div style={{
                                    width: '56px',
                                    height: '56px',
                                    background: `linear-gradient(135deg, ${feature.color}15 0%, ${feature.color}25 100%)`,
                                    borderRadius: '16px',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    margin: '0 auto 1rem',
                                }}>
                                    <feature.icon size={28} style={{ color: feature.color }} />
                                </div>
                                <h3 style={{ fontWeight: 700, color: '#1F2937', marginBottom: '0.5rem' }}>{feature.title}</h3>
                                <p style={{ color: '#6B7280', fontSize: '0.875rem', lineHeight: 1.5 }}>{feature.desc}</p>
                            </motion.div>
                        ))}
                    </motion.div>
                )}
            </main>

            {/* CSS for animations */}
            <style>{`
                @keyframes spin {
                    from { transform: rotate(0deg); }
                    to { transform: rotate(360deg); }
                }
            `}</style>
        </div>
    );
};

export default SymptomSearch;
