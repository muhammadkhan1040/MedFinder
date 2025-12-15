import { motion } from 'framer-motion';
import { Pill, Activity, BookOpen, AlertCircle, TrendingDown, ExternalLink } from 'lucide-react';

/**
 * SymptomSearchResults Component - Premium Redesign
 * 
 * Displays AI analysis results with inline styles
 */
const SymptomSearchResults = ({ results }) => {
    if (!results) return null;

    // NEW FORMAT: Extract recommendations directly
    const recommendations = results.recommendations || [];
    const aiAnalysis = results.ai_analysis || '';
    const ragUsed = results.rag_used || false;
    const ragChunks = results.rag_chunks || 0;

    // Format price
    const formatPrice = (priceStr) => {
        if (!priceStr || priceStr === 'N/A') return 'N/A';
        if (typeof priceStr === 'string' && priceStr.includes('Rs.')) return priceStr;
        const num = parseFloat(String(priceStr).replace(/[^0-9.]/g, ''));
        return isNaN(num) ? 'N/A' : `Rs. ${num.toFixed(2)}`;
    };

    return (
        <div style={{ maxWidth: '64rem', margin: '0 auto' }}>
            {/* AI Summary Card */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                style={{
                    background: 'white',
                    borderRadius: '20px',
                    boxShadow: '0 4px 25px -5px rgba(0, 0, 0, 0.1)',
                    overflow: 'hidden',
                    marginBottom: '2rem',
                    border: '1px solid #E5E7EB',
                }}
            >
                {/* Header */}
                <div style={{
                    background: 'linear-gradient(135deg, rgba(59, 130, 246, 0.08) 0%, rgba(139, 92, 246, 0.08) 100%)',
                    padding: '1.25rem 1.5rem',
                    borderBottom: '1px solid #E5E7EB',
                }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                        <div style={{
                            padding: '0.625rem',
                            background: 'linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%)',
                            borderRadius: '12px',
                        }}>
                            <Activity size={20} style={{ color: 'white' }} />
                        </div>
                        <div>
                            <h2 style={{ fontWeight: 700, color: '#1F2937', fontSize: '1.125rem' }}>
                                AI Analysis Complete {ragUsed && '(RAG Enhanced 🔍)'}
                            </h2>
                            <p style={{ color: '#6B7280', fontSize: '0.875rem' }}>
                                {ragUsed ? `Used ${ragChunks} medical sources` : 'Based on AI medical knowledge'}
                            </p>
                        </div>
                    </div>
                </div>

                {/* AI Response */}
                {aiAnalysis && (
                    <div style={{ padding: '1.5rem' }}>
                        <div style={{ display: 'flex', alignItems: 'flex-start', gap: '0.75rem' }}>
                            <BookOpen size={18} style={{ color: '#8B5CF6', flexShrink: 0, marginTop: '0.125rem' }} />
                            <div>
                                <h3 style={{ fontWeight: 600, color: '#1F2937', fontSize: '0.9375rem', marginBottom: '0.5rem' }}>
                                    Medical Analysis
                                </h3>
                                <p style={{
                                    color: '#4B5563',
                                    fontSize: '0.9375rem',
                                    lineHeight: 1.6,
                                    background: '#F9FAFB',
                                    padding: '1rem',
                                    borderRadius: '12px',
                                    border: '1px solid #E5E7EB',
                                }}>
                                    {aiAnalysis}
                                </p>
                            </div>
                        </div>
                    </div>
                )}
            </motion.div>

            {/* Recommended Medicines */}
            <h2 style={{
                fontSize: '1.5rem',
                fontWeight: 700,
                color: '#1F2937',
                marginBottom: '1.5rem',
                textAlign: 'center',
            }}>
                Recommended Medicines
            </h2>

            {recommendations.length === 0 ? (
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    style={{
                        textAlign: 'center',
                        padding: '3rem',
                        background: 'white',
                        borderRadius: '16px',
                        border: '1px solid #E5E7EB',
                    }}
                >
                    <AlertCircle size={48} style={{ color: '#D1D5DB', margin: '0 auto 1rem' }} />
                    <h3 style={{ fontWeight: 600, color: '#4B5563', marginBottom: '0.5rem' }}>
                        No specific medicines found
                    </h3>
                    <p style={{ color: '#9CA3AF' }}>
                        Try refining your symptoms or consult a doctor.
                    </p>
                </motion.div>
            ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                    {recommendations.map((rec, index) => {
                        const matchedMeds = rec.matched_medicines || [];
                        const chemicalFormula = rec.chemical_formula || 'Unknown';

                        // Calculate price range if medicines available
                        const prices = matchedMeds.map(m => parseFloat(m.price || 0)).filter(p => p > 0);
                        const minPrice = prices.length > 0 ? Math.min(...prices) : null;
                        const maxPrice = prices.length > 0 ? Math.max(...prices) : null;
                        const savingsPercentage = prices.length > 0 && maxPrice > minPrice
                            ? Math.round(((maxPrice - minPrice) / maxPrice) * 100)
                            : 0;

                        return (
                            <motion.div
                                key={index}
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: index * 0.1 }}
                                style={{
                                    background: 'white',
                                    borderRadius: '20px',
                                    boxShadow: '0 4px 25px -5px rgba(0, 0, 0, 0.08)',
                                    overflow: 'hidden',
                                    border: '1px solid #E5E7EB',
                                }}
                            >
                                {/* Formula Header */}
                                <div style={{
                                    padding: '1.25rem 1.5rem',
                                    borderBottom: '1px solid #E5E7EB',
                                    background: 'linear-gradient(135deg, #FAFBFC 0%, white 100%)',
                                }}>
                                    <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: '1rem' }}>
                                        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', flex: 1 }}>
                                            <div style={{
                                                width: '48px',
                                                height: '48px',
                                                background: `linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%)`,
                                                borderRadius: '14px',
                                                display: 'flex',
                                                alignItems: 'center',
                                                justifyContent: 'center',
                                                flexShrink: 0
                                            }}>
                                                <span style={{ color: 'white', fontWeight: 700, fontSize: '1.25rem' }}>
                                                    {rec.rank || index + 1}
                                                </span>
                                            </div>
                                            <div style={{ flex: 1 }}>
                                                <h3 style={{ fontWeight: 700, color: '#1F2937', fontSize: '1.125rem', marginBottom: '0.25rem' }}>
                                                    {chemicalFormula}
                                                </h3>
                                                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem', alignItems: 'center' }}>
                                                    <span style={{ color: '#6B7280', fontSize: '0.875rem' }}>
                                                        {matchedMeds.length} {matchedMeds.length === 1 ? 'product' : 'products'} available
                                                    </span>
                                                    <span style={{
                                                        padding: '0.125rem 0.5rem',
                                                        background: rec.requires_doctor ? '#FEF3C7' : '#D1FAE5',
                                                        color: rec.requires_doctor ? '#92400E' : '#065F46',
                                                        borderRadius: '9999px',
                                                        fontSize: '0.75rem',
                                                        fontWeight: 600
                                                    }}>
                                                        {rec.requires_doctor ? '⚠ Doctor Required' : '✓ OTC'}
                                                    </span>
                                                </div>
                                            </div>
                                        </div>

                                        {minPrice && maxPrice && (
                                            <div style={{ textAlign: 'right' }}>
                                                <p style={{ fontSize: '0.6875rem', color: '#9CA3AF', fontWeight: 600, textTransform: 'uppercase', marginBottom: '0.25rem' }}>
                                                    Price Range
                                                </p>
                                                <p style={{ fontWeight: 700, color: '#1F2937', fontSize: '1rem', fontFamily: "'JetBrains Mono', monospace" }}>
                                                    Rs. {minPrice.toFixed(0)} - {maxPrice.toFixed(0)}
                                                </p>
                                                {savingsPercentage > 0 && (
                                                    <div style={{
                                                        marginTop: '0.25rem',
                                                        padding: '0.25rem 0.5rem',
                                                        background: 'linear-gradient(135deg, #10B981 0%, #34D399 100%)',
                                                        borderRadius: '9999px',
                                                        color: 'white',
                                                        fontSize: '0.75rem',
                                                        fontWeight: 700,
                                                        display: 'inline-flex',
                                                        alignItems: 'center',
                                                        gap: '0.25rem',
                                                    }}>
                                                        <TrendingDown size={12} />
                                                        Save {savingsPercentage}%
                                                    </div>
                                                )}
                                            </div>
                                        )}
                                    </div>

                                    {/* Dosage and Explanation */}
                                    <div style={{ marginTop: '1rem', display: 'grid', gap: '0.75rem' }}>
                                        <div style={{ background: '#F9FAFB', padding: '0.75rem 1rem', borderRadius: '10px', border: '1px solid #E5E7EB' }}>
                                            <p style={{ fontSize: '0.75rem', color: '#6B7280', fontWeight: 600, marginBottom: '0.25rem' }}>Dosage:</p>
                                            <p style={{ fontSize: '0.875rem', color: '#1F2937', fontWeight: 500 }}>{rec.dosage || 'As directed'}</p>
                                        </div>
                                        <div style={{ background: '#EFF6FF', padding: '0.75rem 1rem', borderRadius: '10px', border: '1px solid #DBEAFE' }}>
                                            <p style={{ fontSize: '0.75rem', color: '#1E40AF', fontWeight: 600, marginBottom: '0.25rem' }}>Why it helps:</p>
                                            <p style={{ fontSize: '0.875rem', color: '#1E3A8A', lineHeight: 1.5 }}>{rec.explanation || 'Recommended for your symptoms'}</p>
                                        </div>
                                        <div style={{ background: '#FEF3C7', padding: '0.75rem 1rem', borderRadius: '10px', border: '1px solid #FDE68A' }}>
                                            <p style={{ fontSize: '0.75rem', color: '#92400E', fontWeight: 600, marginBottom: '0.25rem' }}>⚠ Warnings:</p>
                                            <p style={{ fontSize: '0.875rem', color: '#78350F', lineHeight: 1.5 }}>{rec.warnings || 'Consult doctor if symptoms persist'}</p>
                                        </div>
                                    </div>
                                </div>

                                {/* Medicine Grid */}
                                {matchedMeds.length > 0 && (
                                    <div style={{ padding: '1.25rem 1.5rem' }}>
                                        <h4 style={{ fontWeight: 600, color: '#1F2937', marginBottom: '1rem', fontSize: '0.9375rem' }}>
                                            Available Products ({matchedMeds.length})
                                        </h4>
                                        <div style={{
                                            display: 'grid',
                                            gridTemplateColumns: 'repeat(auto-fill, minmax(260px, 1fr))',
                                            gap: '0.875rem',
                                        }}>
                                            {matchedMeds.slice(0, 6).map((med, medIdx) => (
                                                <div
                                                    key={medIdx}
                                                    style={{
                                                        padding: '1rem',
                                                        background: '#F9FAFB',
                                                        borderRadius: '12px',
                                                        border: '1px solid #E5E7EB',
                                                        transition: 'all 0.2s ease',
                                                        cursor: 'pointer',
                                                    }}
                                                    onMouseEnter={(e) => {
                                                        e.currentTarget.style.borderColor = '#3B82F6';
                                                        e.currentTarget.style.background = 'rgba(59, 130, 246, 0.05)';
                                                    }}
                                                    onMouseLeave={(e) => {
                                                        e.currentTarget.style.borderColor = '#E5E7EB';
                                                        e.currentTarget.style.background = '#F9FAFB';
                                                    }}
                                                >
                                                    <div style={{ marginBottom: '0.5rem' }}>
                                                        <h5 style={{ fontWeight: 600, color: '#1F2937', fontSize: '0.9375rem', marginBottom: '0.25rem' }}>
                                                            {med.name}
                                                        </h5>
                                                        <p style={{ fontSize: '0.75rem', color: '#6B7280' }}>
                                                            {med.manufacturer || 'Unknown maker'}
                                                        </p>
                                                        <p style={{ fontSize: '0.75rem', color: '#9CA3AF', marginTop: '0.125rem' }}>
                                                            {med.pack_size || 'Pack size varies'}
                                                        </p>
                                                    </div>
                                                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                                        <span style={{ fontSize: '0.75rem', color: '#6B7280' }}>
                                                            {med.formula}
                                                        </span>
                                                        <span style={{
                                                            fontWeight: 700,
                                                            color: '#1F2937',
                                                            fontSize: '0.875rem',
                                                            fontFamily: "'JetBrains Mono', monospace",
                                                            background: 'white',
                                                            padding: '0.25rem 0.5rem',
                                                            borderRadius: '6px',
                                                            border: '1px solid #E5E7EB',
                                                        }}>
                                                            {formatPrice(med.price)}
                                                        </span>
                                                    </div>
                                                </div>
                                            ))}
                                        </div>

                                        {matchedMeds.length > 6 && (
                                            <button style={{
                                                width: '100%',
                                                marginTop: '1rem',
                                                padding: '0.75rem',
                                                background: 'transparent',
                                                color: '#3B82F6',
                                                border: '1px dashed #3B82F6',
                                                borderRadius: '10px',
                                                fontWeight: 600,
                                                fontSize: '0.875rem',
                                                cursor: 'pointer',
                                            }}>
                                                View all {matchedMeds.length} medicines →
                                            </button>
                                        )}
                                    </div>
                                )}
                            </motion.div>
                        );
                    })}
                </div>
            )}

            {/* Disclaimer */}
            <div style={{
                marginTop: '2rem',
                padding: '1rem 1.5rem',
                background: 'rgba(251, 191, 36, 0.1)',
                border: '1px solid rgba(251, 191, 36, 0.3)',
                borderRadius: '12px',
                textAlign: 'center',
            }}>
                <p style={{ color: '#92400E', fontSize: '0.8125rem', lineHeight: 1.6 }}>
                    <strong>Disclaimer:</strong> This AI assistant provides information based on pharmacological data
                    but is not a substitute for professional medical advice. Always consult a doctor before taking medication.
                </p>
            </div>
        </div>
    );
};

export default SymptomSearchResults;
