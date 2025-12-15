import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Pill, Search, AlertTriangle, CheckCircle, XCircle, ExternalLink,
    Loader2, Info, Sparkles, AlertCircle, Plus, X, Zap,
    Shield, Activity, FileText, Clock, BookOpen
} from 'lucide-react';

/**
 * Prescription Assistant Component - MedFinder Edition
 * 
 * Features:
 * - Drug information search from FDA/NIH/DailyMed
 * - Drug interaction checking
 * - AI-powered drug name validation
 * - White and purple theme matching MedFinder design
 */
export default function PrescriptionAssistant() {
    // Search state
    const [drugName, setDrugName] = useState('');
    const [searchType, setSearchType] = useState('drug'); // 'drug', 'interaction'
    const [loading, setLoading] = useState(false);
    const [results, setResults] = useState(null);
    const [error, setError] = useState('');

    // Interaction check state (for multiple drugs)
    const [interactionDrugs, setInteractionDrugs] = useState(['', '']);
    const [interactionResults, setInteractionResults] = useState(null);
    const [showAllSuggestions, setShowAllSuggestions] = useState(false);

    const handleSearch = async (e) => {
        e?.preventDefault();
        if (!drugName.trim()) return;

        setLoading(true);
        setError('');
        setResults(null);
        setShowAllSuggestions(false);

        try {
            const response = await fetch('http://localhost:5000/api/prescription/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    drug_name: drugName.trim(),
                    search_type: 'drug'
                })
            });

            if (!response.ok) {
                throw new Error('Failed to fetch prescription information');
            }

            const data = await response.json();
            setResults(data);
        } catch (err) {
            setError(err.message || 'Error searching prescription information');
        } finally {
            setLoading(false);
        }
    };

    const handleInteractionCheck = async () => {
        const validDrugs = interactionDrugs.filter(d => d.trim().length > 0);
        if (validDrugs.length < 2) {
            setError('Please enter at least 2 drugs to check interactions');
            return;
        }

        setLoading(true);
        setError('');
        setInteractionResults(null);

        try {
            const response = await fetch('http://localhost:5000/api/prescription/interaction-check', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(validDrugs)
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.detail || 'Failed to check interactions');
            }

            const data = await response.json();
            setInteractionResults(data);
        } catch (err) {
            setError(err.message || 'Error checking drug interactions');
        } finally {
            setLoading(false);
        }
    };

    const addInteractionDrug = () => {
        if (interactionDrugs.length < 5) {
            setInteractionDrugs([...interactionDrugs, '']);
        }
    };

    const removeInteractionDrug = (index) => {
        if (interactionDrugs.length > 2) {
            setInteractionDrugs(interactionDrugs.filter((_, i) => i !== index));
        }
    };

    const updateInteractionDrug = (index, value) => {
        const updated = [...interactionDrugs];
        updated[index] = value;
        setInteractionDrugs(updated);
    };

    const getSeverityColor = (severity) => {
        const s = severity?.toLowerCase() || '';
        if (s.includes('high') || s.includes('major') || s.includes('serious'))
            return { bg: '#FEE2E2', text: '#991B1B', border: '#FCA5A5' };
        if (s.includes('moderate') || s.includes('medium'))
            return { bg: '#FEF3C7', text: '#92400E', border: '#FCD34D' };
        return { bg: '#DBEAFE', text: '#1E40AF', border: '#93C5FD' };
    };

    return (
        <div style={{
            minHeight: '100vh',
            background: 'linear-gradient(135deg, #FAFBFC 0%, #F3F4F6 100%)',
            paddingTop: '6rem',
            paddingBottom: '4rem'
        }}>
            <div style={{ maxWidth: '72rem', margin: '0 auto', padding: '0 2rem' }}>
                {/* Hero Header */}
                <motion.div
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    style={{ textAlign: 'center', marginBottom: '3.5rem' }}
                >
                    <div style={{
                        display: 'inline-flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        padding: '1.25rem',
                        background: 'linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%)',
                        borderRadius: '24px',
                        marginBottom: '1.75rem',
                        boxShadow: '0 10px 40px -10px rgba(124, 58, 237, 0.5)',
                        transform: 'translateY(0)',
                        transition: 'transform 0.3s ease'
                    }}>
                        <Pill size={40} style={{ color: 'white' }} />
                    </div>
                    <h1 style={{
                        fontSize: 'clamp(2.5rem, 5vw, 3.5rem)',
                        fontWeight: 800,
                        background: 'linear-gradient(135deg, #1F2937 0%, #7C3AED 50%, #A855F7 100%)',
                        WebkitBackgroundClip: 'text',
                        WebkitTextFillColor: 'transparent',
                        marginBottom: '1.25rem',
                        letterSpacing: '-0.02em',
                        lineHeight: 1.1
                    }}>
                        Prescription Assistant
                    </h1>
                    <p style={{
                        color: '#6B7280',
                        fontSize: '1.25rem',
                        maxWidth: '45rem',
                        margin: '0 auto',
                        lineHeight: 1.7,
                        fontWeight: 400
                    }}>
                        Evidence-based drug information from <span style={{ color: '#7C3AED', fontWeight: 600 }}>NIH</span>, <span style={{ color: '#7C3AED', fontWeight: 600 }}>FDA</span>, and trusted medical sources
                    </p>
                </motion.div>

                {/* Search Type Toggle */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.1 }}
                    style={{
                        display: 'flex',
                        gap: '0.625rem',
                        padding: '0.5rem',
                        background: 'white',
                        borderRadius: '20px',
                        width: 'fit-content',
                        margin: '0 auto 3rem',
                        boxShadow: '0 4px 25px -5px rgba(0, 0, 0, 0.12)',
                        border: '1px solid rgba(124, 58, 237, 0.1)'
                    }}
                >
                    <button
                        onClick={() => { setSearchType('drug'); setResults(null); setInteractionResults(null); setError(''); }}
                        style={{
                            padding: '1rem 2rem',
                            borderRadius: '16px',
                            fontWeight: 600,
                            fontSize: '1rem',
                            border: 'none',
                            cursor: 'pointer',
                            transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '0.625rem',
                            ...(searchType === 'drug' ? {
                                background: 'linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%)',
                                color: 'white',
                                boxShadow: '0 8px 20px rgba(124, 58, 237, 0.35)',
                                transform: 'translateY(-1px)'
                            } : {
                                background: 'transparent',
                                color: '#6B7280',
                                transform: 'translateY(0)'
                            })
                        }}
                        onMouseEnter={(e) => {
                            if (searchType !== 'drug') {
                                e.target.style.background = '#F9FAFB';
                                e.target.style.color = '#374151';
                            }
                        }}
                        onMouseLeave={(e) => {
                            if (searchType !== 'drug') {
                                e.target.style.background = 'transparent';
                                e.target.style.color = '#6B7280';
                            }
                        }}
                    >
                        <Search size={18} />
                        Drug Search
                    </button>
                    <button
                        onClick={() => { setSearchType('interaction'); setResults(null); setInteractionResults(null); setError(''); }}
                        style={{
                            padding: '1rem 2rem',
                            borderRadius: '16px',
                            fontWeight: 600,
                            fontSize: '1rem',
                            border: 'none',
                            cursor: 'pointer',
                            transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '0.625rem',
                            ...(searchType === 'interaction' ? {
                                background: 'linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%)',
                                color: 'white',
                                boxShadow: '0 8px 20px rgba(124, 58, 237, 0.35)',
                                transform: 'translateY(-1px)'
                            } : {
                                background: 'transparent',
                                color: '#6B7280',
                                transform: 'translateY(0)'
                            })
                        }}
                        onMouseEnter={(e) => {
                            if (searchType !== 'interaction') {
                                e.target.style.background = '#F9FAFB';
                                e.target.style.color = '#374151';
                            }
                        }}
                        onMouseLeave={(e) => {
                            if (searchType !== 'interaction') {
                                e.target.style.background = 'transparent';
                                e.target.style.color = '#6B7280';
                            }
                        }}
                    >
                        <Zap size={18} />
                        Interaction Check
                    </button>
                </motion.div>

                {/* Drug Search Form */}
                {searchType === 'drug' && (
                    <motion.form
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.2 }}
                        onSubmit={handleSearch}
                        style={{
                            background: 'white',
                            borderRadius: '24px',
                            padding: '3rem',
                            boxShadow: '0 4px 30px -5px rgba(0, 0, 0, 0.1)',
                            border: '1px solid rgba(124, 58, 237, 0.08)',
                            marginBottom: '2.5rem'
                        }}
                    >
                        <div style={{ marginBottom: '2rem' }}>
                            <label style={{
                                display: 'block',
                                fontSize: '0.9375rem',
                                fontWeight: 600,
                                color: '#374151',
                                marginBottom: '0.875rem',
                                letterSpacing: '-0.01em'
                            }}>
                                Drug Name
                            </label>
                            <input
                                type="text"
                                value={drugName}
                                onChange={(e) => setDrugName(e.target.value)}
                                placeholder="e.g., Aspirin, Metformin, Lisinopril, Amoxic illin..."
                                required
                                autoComplete="off"
                                style={{
                                    width: '100%',
                                    padding: '1.125rem 1.5rem',
                                    background: '#F9FAFB',
                                    border: '2px solid #E5E7EB',
                                    borderRadius: '16px',
                                    fontSize: '1.0625rem',
                                    color: '#1F2937',
                                    outline: 'none',
                                    transition: 'all 0.2s cubic-bezier(0.4, 0, 0.2, 1)',
                                    fontWeight: 400
                                }}
                                onFocus={(e) => {
                                    e.target.style.borderColor = '#7C3AED';
                                    e.target.style.background = 'white';
                                    e.target.style.boxShadow = '0 0 0 4px rgba(124, 58, 237, 0.08)';
                                }}
                                onBlur={(e) => {
                                    e.target.style.borderColor = '#E5E7EB';
                                    e.target.style.background = '#F9FAFB';
                                    e.target.style.boxShadow = 'none';
                                }}
                            />
                        </div>

                        <button
                            type="submit"
                            disabled={loading || !drugName.trim()}
                            style={{
                                width: '100%',
                                padding: '1.125rem 1.5rem',
                                background: loading || !drugName.trim()
                                    ? 'linear-gradient(135deg, #D1D5DB 0%, #9CA3AF 100%)'
                                    : 'linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%)',
                                borderRadius: '16px',
                                fontWeight: 600,
                                fontSize: '1.0625rem',
                                color: 'white',
                                border: 'none',
                                cursor: loading || !drugName.trim() ? 'not-allowed' : 'pointer',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                gap: '0.625rem',
                                boxShadow: loading || !drugName.trim() ? 'none' : '0 8px 20px rgba(124, 58, 237, 0.3)',
                                transition: 'all 0.2s ease',
                                transform: 'translateY(0)'
                            }}
                            onMouseEnter={(e) => {
                                if (!loading && drugName.trim()) {
                                    e.target.style.transform = 'translateY(-2px)';
                                    e.target.style.boxShadow = '0 12px 28px rgba(124, 58, 237, 0.4)';
                                }
                            }}
                            onMouseLeave={(e) => {
                                e.target.style.transform = 'translateY(0)';
                                e.target.style.boxShadow = loading || !drugName.trim() ? 'none' : '0 8px 20px rgba(124, 58, 237, 0.3)';
                            }}
                        >
                            {loading ? (
                                <>
                                    <Loader2 size={20} style={{ animation: 'spin 1s linear infinite' }} />
                                    Searching trusted sources...
                                </>
                            ) : (
                                <>
                                    <Search size={20} />
                                    Search Drug Information
                                </>
                            )}
                        </button>

                        <p style={{
                            textAlign: 'center',
                            fontSize: '0.8125rem',
                            color: '#9CA3AF',
                            marginTop: '1.25rem',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            gap: '0.5rem'
                        }}>
                            <Shield size={14} style={{ color: '#10B981' }} />
                            Sources: RxNorm (NIH) •  OpenFDA • DailyMed
                        </p>

                        {/* Animation */}
                        <style>{`
                            @keyframes spin {
                                from { transform: rotate(0deg); }
                                to { transform: rotate(360deg); }
                            }
                        `}</style>
                    </motion.form>
                )}

                {/* Interaction Check Form */}
                {searchType === 'interaction' && (
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.2 }}
                        style={{
                            background: 'white',
                            borderRadius: '24px',
                            padding: '3rem',
                            boxShadow: '0 4px 30px -5px rgba(0, 0, 0, 0.1)',
                            border: '1px solid rgba(245, 158, 11, 0.15)',
                            marginBottom: '2.5rem'
                        }}
                    >
                        <div style={{ marginBottom: '2rem' }}>
                            <label style={{
                                display: 'block',
                                fontSize: '0.9375rem',
                                fontWeight: 600,
                                color: '#374151',
                                marginBottom: '1rem',
                                letterSpacing: '-0.01em'
                            }}>
                                Enter drugs to check for interactions
                            </label>
                            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                                {interactionDrugs.map((drug, index) => (
                                    <div key={index} style={{ display: 'flex', gap: '0.75rem', alignItems: 'center' }}>
                                        <input
                                            type="text"
                                            value={drug}
                                            onChange={(e) => updateInteractionDrug(index, e.target.value)}
                                            placeholder={`Drug ${index + 1} (e.g., ${index === 0 ? 'Warfarin' : index === 1 ? 'Aspirin' : 'Ibuprofen'})`}
                                            style={{
                                                flex: 1,
                                                padding: '1.125rem 1.5rem',
                                                background: '#F9FAFB',
                                                border: '2px solid #E5E7EB',
                                                borderRadius: '16px',
                                                fontSize: '1.0625rem',
                                                color: '#1F2937',
                                                outline: 'none',
                                                transition: 'all 0.2s cubic-bezier(0.4, 0, 0.2, 1)',
                                                fontWeight: 400
                                            }}
                                            onFocus={(e) => {
                                                e.target.style.borderColor = '#F59E0B';
                                                e.target.style.background = 'white';
                                                e.target.style.boxShadow = '0 0 0 4px rgba(245, 158, 11, 0.08)';
                                            }}
                                            onBlur={(e) => {
                                                e.target.style.borderColor = '#E5E7EB';
                                                e.target.style.background = '#F9FAFB';
                                                e.target.style.boxShadow = 'none';
                                            }}
                                        />
                                        {interactionDrugs.length > 2 && (
                                            <button
                                                type="button"
                                                onClick={() => removeInteractionDrug(index)}
                                                style={{
                                                    padding: '1rem',
                                                    background: '#FEE2E2',
                                                    color: '#DC2626',
                                                    border: 'none',
                                                    borderRadius: '14px',
                                                    cursor: 'pointer',
                                                    transition: 'all 0.2s ease',
                                                    display: 'flex',
                                                    alignItems: 'center',
                                                    justifyContent: 'center'
                                                }}
                                                onMouseEnter={(e) => {
                                                    e.target.style.background = '#FCA5A5';
                                                }}
                                                onMouseLeave={(e) => {
                                                    e.target.style.background = '#FEE2E2';
                                                }}
                                            >
                                                <X size={20} />
                                            </button>
                                        )}
                                    </div>
                                ))}
                            </div>

                            {interactionDrugs.length < 5 && (
                                <button
                                    type="button"
                                    onClick={addInteractionDrug}
                                    style={{
                                        marginTop: '1.25rem',
                                        display: 'flex',
                                        alignItems: 'center',
                                        gap: '0.5rem',
                                        color: '#F59E0B',
                                        fontSize: '0.9375rem',
                                        fontWeight: 600,
                                        background: 'transparent',
                                        border: 'none',
                                        cursor: 'pointer',
                                        transition: 'color 0.2s ease'
                                    }}
                                    onMouseEnter={(e) => e.target.style.color = '#D97706'}
                                    onMouseLeave={(e) => e.target.style.color = '#F59E0B'}
                                >
                                    <Plus size={16} />
                                    Add another drug (up to 5)
                                </button>
                            )}
                        </div>

                        <button
                            onClick={handleInteractionCheck}
                            disabled={loading || interactionDrugs.filter(d => d.trim()).length < 2}
                            style={{
                                width: '100%',
                                padding: '1.125rem 1.5rem',
                                background: loading || interactionDrugs.filter(d => d.trim()).length < 2
                                    ? 'linear-gradient(135deg, #D1D5DB 0%, #9CA3AF 100%)'
                                    : 'linear-gradient(135deg, #F59E0B 0%, #D97706 100%)',
                                borderRadius: '16px',
                                fontWeight: 600,
                                fontSize: '1.0625rem',
                                color: 'white',
                                border: 'none',
                                cursor: loading || interactionDrugs.filter(d => d.trim()).length < 2 ? 'not-allowed' : 'pointer',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                gap: '0.625rem',
                                boxShadow: loading || interactionDrugs.filter(d => d.trim()).length < 2 ? 'none' : '0 8px 20px rgba(245, 158, 11, 0.3)',
                                transition: 'all 0.2s ease',
                                transform: 'translateY(0)'
                            }}
                            onMouseEnter={(e) => {
                                if (!loading && interactionDrugs.filter(d => d.trim()).length >= 2) {
                                    e.target.style.transform = 'translateY(-2px)';
                                    e.target.style.boxShadow = '0 12px 28px rgba(245, 158, 11, 0.4)';
                                }
                            }}
                            onMouseLeave={(e) => {
                                e.target.style.transform = 'translateY(0)';
                                e.target.style.boxShadow = loading || interactionDrugs.filter(d => d.trim()).length < 2 ? 'none' : '0 8px 20px rgba(245, 158, 11, 0.3)';
                            }}
                        >
                            {loading ? (
                                <>
                                    <Loader2 size={20} style={{ animation: 'spin 1s linear infinite' }} />
                                    Checking interactions...
                                </>
                            ) : (
                                <>
                                    <Zap size={20} />
                                    Check Drug Interactions
                                </>
                            )}
                        </button>
                    </motion.div>
                )}

                {/* Error */}
                <AnimatePresence>
                    {error && (
                        <motion.div
                            initial={{ opacity: 0, y: -10 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -10 }}
                            className="bg-red-50 border border-red-200 rounded-xl p-4 flex items-center gap-3"
                        >
                            <XCircle className="w-5 h-5 text-red-600 shrink-0" />
                            <p className="text-red-700">{error}</p>
                        </motion.div>
                    )}
                </AnimatePresence>

                {/* Spelling Suggestion / Did You Mean */}
                {results?.spelling_suggestion && !results.drug_found && (
                    <motion.div
                        initial={{ opacity: 0, scale: 0.95 }}
                        animate={{ opacity: 1, scale: 1 }}
                        className="bg-gradient-to-r from-amber-50 to-yellow-50 border border-yellow-300 rounded-xl p-6"
                    >
                        <div className="flex items-start gap-3">
                            <div className="p-2 bg-yellow-100 rounded-lg">
                                <Sparkles className="w-5 h-5 text-yellow-600" />
                            </div>
                            <div className="flex-1">
                                <h3 className="text-yellow-900 font-semibold mb-2">Did you mean?</h3>
                                <p className="text-gray-700 text-sm mb-3">
                                    We couldn't find "<span className="font-medium text-gray-900">{drugName}</span>".
                                    Try one of these suggestions:
                                </p>
                                <div className="flex flex-wrap gap-2">
                                    {(showAllSuggestions
                                        ? results.spelling_suggestion.suggestions
                                        : results.spelling_suggestion.suggestions.slice(0, 5)
                                    ).map((s, i) => (
                                        <button
                                            key={i}
                                            onClick={() => { setDrugName(s); setTimeout(() => handleSearch(), 100); }}
                                            className="px-4 py-2 bg-white hover:bg-yellow-100 border border-yellow-300 rounded-lg font-medium text-yellow-800 transition-all hover:scale-105 shadow-sm"
                                        >
                                            {s}
                                        </button>
                                    ))}
                                    {results.spelling_suggestion.suggestions.length > 5 && (
                                        <button
                                            onClick={() => setShowAllSuggestions(!showAllSuggestions)}
                                            className="px-4 py-2 text-yellow-700 hover:text-yellow-900 text-sm font-medium transition-colors"
                                        >
                                            {showAllSuggestions ? 'Show Less' : `+ ${results.spelling_suggestion.suggestions.length - 5} More`}
                                        </button>
                                    )}
                                </div>
                            </div>
                        </div>
                    </motion.div>
                )}

                {/* Drug Search Results */}
                {results?.drug_found && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}
                    >
                        {/* Drug Header */}
                        <div style={{
                            background: 'linear-gradient(135deg, rgba(124, 58, 237, 0.08) 0%, rgba(168, 85, 247, 0.08) 100%)',
                            border: '1px solid rgba(124, 58, 237, 0.2)',
                            borderRadius: '24px',
                            padding: '2.5rem'
                        }}>
                            <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1rem' }}>
                                <div style={{ flex: 1 }}>
                                    <h2 style={{
                                        fontSize: 'clamp(1.75rem, 3vw, 2.25rem)',
                                        fontWeight: 800,
                                        background: 'linear-gradient(135deg, #7C3AED 0%, #A855F7 100%)',
                                        WebkitBackgroundClip: 'text',
                                        WebkitTextFillColor: 'transparent',
                                        marginBottom: '0.75rem',
                                        letterSpacing: '-0.02em'
                                    }}>
                                        {results.query}
                                    </h2>
                                    {results.drug_info?.rxcui && (
                                        <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap', alignItems: 'center' }}>
                                            <span style={{
                                                fontSize: '0.875rem',
                                                color: '#6B7280',
                                                fontFamily: "'JetBrains Mono', monospace",
                                                background: 'white',
                                                padding: '0.375rem 0.75rem',
                                                borderRadius: '8px',
                                                border: '1px solid #E5E7EB'
                                            }}>
                                                RxCUI: {results.drug_info.rxcui}
                                            </span>
                                            <span style={{
                                                fontSize: '0.875rem',
                                                color: '#7C3AED',
                                                fontWeight: 600,
                                                background: 'white',
                                                padding: '0.375rem 0.75rem',
                                                borderRadius: '8px',
                                                border: '1px solid rgba(124, 58, 237, 0.2)'
                                            }}>
                                                {results.drug_info.tty || 'Drug'}
                                            </span>
                                        </div>
                                    )}
                                </div>
                                <div style={{
                                    display: 'flex',
                                    alignItems: 'center',
                                    gap: '0.5rem',
                                    fontSize: '0.8125rem',
                                    color: '#9CA3AF',
                                    background: 'white',
                                    padding: '0.5rem 1rem',
                                    borderRadius: '9999px'
                                }}>
                                    <Clock size={14} />
                                    {results.search_time_ms}ms
                                </div>
                            </div>
                        </div>

                        {/* Indications */}
                        {results.indications?.length > 0 && (
                            <div style={{
                                background: 'white',
                                border: '1px solid #E5E7EB',
                                borderRadius: '20px',
                                padding: '2.5rem',
                                boxShadow: '0 4px 25px -5px rgba(0, 0, 0, 0.08)'
                            }}>
                                <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1.75rem' }}>
                                    <div style={{
                                        padding: '0.625rem',
                                        background: 'linear-gradient(135deg, #10B981 0%, #34D399 100%)',
                                        borderRadius: '12px'
                                    }}>
                                        <CheckCircle size={20} style={{ color: 'white' }} />
                                    </div>
                                    <h3 style={{ fontSize: '1.375rem', fontWeight: 700, color: '#1F2937', letterSpacing: '-0.01em' }}>
                                        Indications & Uses
                                    </h3>
                                </div>
                                <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                                    {results.indications.map((ind, idx) => (
                                        <div
                                            key={idx}
                                            style={{
                                                padding: '1.25rem 1.5rem',
                                                background: 'linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%)',
                                                borderLeft: '4px solid #10B981',
                                                borderRadius: '12px',
                                                fontSize: '1rem',
                                                color: '#065F46',
                                                lineHeight: 1.7,
                                                fontWeight: 500
                                            }}
                                        >
                                            {ind}
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                        {/* Dosage */}
                        {results.dosage_forms?.length > 0 && (
                            <div style={{
                                background: 'white',
                                border: '1px solid #E5E7EB',
                                borderRadius: '20px',
                                padding: '2.5rem',
                                boxShadow: '0 4px 25px -5px rgba(0, 0, 0, 0.08)'
                            }}>
                                <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1.75rem' }}>
                                    <div style={{
                                        padding: '0.625rem',
                                        background: 'linear-gradient(135deg, #3B82F6 0%, #60A5FA 100%)',
                                        borderRadius: '12px'
                                    }}>
                                        <Info size={20} style={{ color: 'white' }} />
                                    </div>
                                    <h3 style={{ fontSize: '1.375rem', fontWeight: 700, color: '#1F2937', letterSpacing: '-0.01em' }}>
                                        Dosage & Administration
                                    </h3>
                                </div>
                                <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                                    {results.dosage_forms.map((d, idx) => (
                                        <div
                                            key={idx}
                                            style={{
                                                padding: '1.25rem 1.5rem',
                                                background: 'linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%)',
                                                border: '1px solid #BFDBFE',
                                                borderRadius: '12px',
                                                fontSize: '1rem',
                                                color: '#1E40AF',
                                                lineHeight: 1.7,
                                                fontWeight: 500
                                            }}
                                        >
                                            {d.instructions}
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                        {/* Warnings & Contraindications */}
                        {(results.warnings?.length > 0 || results.contraindications?.length > 0) && (
                            <div style={{
                                background: 'white',
                                border: '1px solid #FECACA',
                                borderRadius: '20px',
                                padding: '2.5rem',
                                boxShadow: '0 4px 25px -5px rgba(239, 68, 68, 0.15)'
                            }}>
                                <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1.75rem' }}>
                                    <div style={{
                                        padding: '0.625rem',
                                        background: 'linear-gradient(135deg, #EF4444 0%, #F87171 100%)',
                                        borderRadius: '12px'
                                    }}>
                                        <AlertTriangle size={20} style={{ color: 'white' }} />
                                    </div>
                                    <h3 style={{ fontSize: '1.375rem', fontWeight: 700, color: '#1F2937', letterSpacing: '-0.01em' }}>
                                        Warnings & Contraindications
                                    </h3>
                                </div>

                                {results.warnings?.filter(w => w.type === 'blackbox').length > 0 && (
                                    <div style={{
                                        marginBottom: '1.5rem',
                                        padding: '1.5rem',
                                        background: 'linear-gradient(135deg, #FEE2E2 0%, #FECACA 100%)',
                                        border: '2px solid #DC2626',
                                        borderRadius: '16px'
                                    }}>
                                        <p style={{
                                            display: 'flex',
                                            alignItems: 'center',
                                            gap: '0.5rem',
                                            color: '#991B1B',
                                            fontWeight: 700,
                                            fontSize: '1rem',
                                            marginBottom: '1rem',
                                            textTransform: 'uppercase',
                                            letterSpacing: '0.05em'
                                        }}>
                                            <AlertCircle size={18} />
                                            BLACK BOX WARNING
                                        </p>
                                        {results.warnings.filter(w => w.type === 'blackbox').map((w, idx) => (
                                            <p key={idx} style={{
                                                color: '#7F1D1D',
                                                fontSize: '1rem',
                                                lineHeight: 1.7,
                                                fontWeight: 500
                                            }}>
                                                {w.description}
                                            </p>
                                        ))}
                                    </div>
                                )}

                                <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                                    {results.contraindications?.map((c, idx) => (
                                        <div
                                            key={idx}
                                            style={{
                                                padding: '1.25rem 1.5rem',
                                                background: 'linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%)',
                                                borderLeft: '4px solid #DC2626',
                                                borderRadius: '12px',
                                                fontSize: '1rem',
                                                color: '#991B1B',
                                                lineHeight: 1.7,
                                                fontWeight: 500
                                            }}
                                        >
                                            {c}
                                        </div>
                                    ))}
                                    {results.warnings?.filter(w => w.type !== 'blackbox').map((w, idx) => (
                                        <div
                                            key={`w-${idx}`}
                                            style={{
                                                padding: '1.25rem 1.5rem',
                                                background: 'linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%)',
                                                borderLeft: '4px solid #F59E0B',
                                                borderRadius: '12px',
                                                fontSize: '1rem',
                                                color: '#92400E',
                                                lineHeight: 1.7,
                                                fontWeight: 500
                                            }}
                                        >
                                            {w.description}
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                        {/* Drug Interactions */}
                        {results.interactions?.length > 0 && (
                            <div className="bg-white border border-yellow-200 rounded-xl p-6 shadow-sm">
                                <div className="flex items-center gap-2 mb-4">
                                    <Zap className="w-5 h-5 text-yellow-600" />
                                    <h3 className="text-lg font-semibold text-gray-900">Known Drug Interactions</h3>
                                    <span className="px-2 py-0.5 bg-yellow-100 text-yellow-700 text-xs rounded-full font-medium">
                                        {results.interactions.length} found
                                    </span>
                                </div>
                                <div className="space-y-3 max-h-96 overflow-y-auto">
                                    {results.interactions.map((int, idx) => (
                                        <div key={idx} className="p-4 bg-gray-50 rounded-lg border border-gray-200">
                                            <div className="flex items-center gap-2 mb-2">
                                                <span className="font-medium text-gray-900">{int.drug2}</span>
                                                <span className={`px-2 py-0.5 rounded text-xs border font-medium ${getSeverityColor(int.severity)}`}>
                                                    {int.severity}
                                                </span>
                                            </div>
                                            <p className="text-sm text-gray-600">{int.description}</p>
                                            <p className="text-xs text-gray-500 mt-2">Source: {int.source}</p>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                        {/* Side Effects */}
                        {results.side_effects?.length > 0 && (
                            <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
                                <div className="flex items-center gap-2 mb-4">
                                    <Activity className="w-5 h-5 text-purple-600" />
                                    <h3 className="text-lg font-semibold text-gray-900">Reported Side Effects</h3>
                                </div>
                                <div className="flex flex-wrap gap-2">
                                    {results.side_effects.map((effect, idx) => (
                                        <span key={idx} className="px-3 py-1.5 bg-gray-100 text-gray-700 text-sm rounded-lg border border-gray-200">
                                            {effect}
                                        </span>
                                    ))}
                                </div>
                            </div>
                        )}

                        {/* Sources */}
                        {results.sources?.length > 0 && (
                            <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
                                <div className="flex items-center gap-2 mb-4">
                                    <FileText className="w-5 h-5 text-indigo-600" />
                                    <h3 className="text-lg font-semibold text-gray-900">Trusted Sources</h3>
                                </div>
                                <div className="grid gap-2 sm:grid-cols-2">
                                    {results.sources.map((source, idx) => (
                                        <a
                                            key={idx}
                                            href={source.url}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors group border border-gray-200"
                                        >
                                            <div className="flex items-center gap-2">
                                                <Shield className="w-4 h-4 text-green-600" />
                                                <span className="text-sm text-gray-700 font-medium">{source.name}</span>
                                            </div>
                                            <ExternalLink className="w-4 h-4 text-gray-400 group-hover:text-purple-600 transition-colors" />
                                        </a>
                                    ))}
                                </div>
                            </div>
                        )}
                    </motion.div>
                )}

                {/* Interaction Check Results */}
                {interactionResults && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}
                    >
                        {/* Analysis Header */}
                        <div style={{
                            background: 'linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(217, 119, 6, 0.1) 100%)',
                            border: '1px solid rgba(245, 158, 11, 0.3)',
                            borderRadius: '24px',
                            padding: '2.5rem'
                        }}>
                            <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1rem' }}>
                                <div style={{ flex: 1 }}>
                                    <h2 style={{
                                        fontSize: 'clamp(1.75rem, 3vw, 2.25rem)',
                                        fontWeight: 800,
                                        background: 'linear-gradient(135deg, #F59E0B 0%, #D97706 100%)',
                                        WebkitBackgroundClip: 'text',
                                        WebkitTextFillColor: 'transparent',
                                        marginBottom: '1rem',
                                        letterSpacing: '-0.02em'
                                    }}>
                                        Drug Interaction Analysis
                                    </h2>
                                    <p style={{
                                        fontSize: '1.0625rem',
                                        color: '#6B7280',
                                        fontWeight: 500
                                    }}>
                                        Analyzed: <span style={{
                                            color: '#D97706',
                                            fontWeight: 700,
                                            fontSize: '1.125rem'
                                        }}>{interactionResults.drugs_checked?.join(' + ')}</span>
                                    </p>
                                </div>
                                <div style={{
                                    display: 'flex',
                                    alignItems: 'center',
                                    gap: '0.5rem',
                                    fontSize: '0.8125rem',
                                    color: '#9CA3AF',
                                    background: 'white',
                                    padding: '0.5rem 1rem',
                                    borderRadius: '9999px'
                                }}>
                                    <Clock size={14} />
                                    {interactionResults.search_time_ms}ms
                                </div>
                            </div>
                        </div>

                        {/* Spelling Corrections */}
                        {interactionResults.had_corrections && interactionResults.spelling_corrections && (
                            <div style={{
                                background: 'linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%)',
                                border: '1px solid #FCD34D',
                                borderRadius: '20px',
                                padding: '2rem'
                            }}>
                                <div style={{ display: 'flex', alignItems: 'flex-start', gap: '1rem' }}>
                                    <div style={{
                                        padding: '0.625rem',
                                        background: 'linear-gradient(135deg, #FBBF24 0%, #F59E0B 100%)',
                                        borderRadius: '12px',
                                        flexShrink: 0
                                    }}>
                                        <Sparkles size={20} style={{ color: 'white' }} />
                                    </div>
                                    <div style={{ flex: 1 }}>
                                        <h4 style={{
                                            fontSize: '1.125rem',
                                            fontWeight: 700,
                                            color: '#92400E',
                                            marginBottom: '1rem'
                                        }}>
                                            Auto-corrected drug names:
                                        </h4>
                                        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                                            {Object.entries(interactionResults.spelling_corrections).map(([original, data]) => (
                                                <div key={original} style={{
                                                    display: 'flex',
                                                    alignItems: 'center',
                                                    gap: '0.75rem',
                                                    fontSize: '1rem',
                                                    flexWrap: 'wrap'
                                                }}>
                                                    <span style={{
                                                        color: '#9CA3AF',
                                                        textDecoration: 'line-through',
                                                        fontWeight: 500
                                                    }}>{original}</span>
                                                    <span style={{ color: '#D1D5DB', fontSize: '1.25rem' }}>→</span>
                                                    <span style={{
                                                        color: '#92400E',
                                                        fontWeight: 700,
                                                        fontSize: '1.0625rem'
                                                    }}>{data.corrected || data.suggestions?.[0]}</span>
                                                    {data.suggestions?.length > 1 && (
                                                        <span style={{
                                                            color: '#A78BFA',
                                                            fontSize: '0.875rem',
                                                            fontStyle: 'italic'
                                                        }}>
                                                            (also: {data.suggestions.slice(1, 3).join(', ')})
                                                        </span>
                                                    )}
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        )}

                        {interactionResults.interactions_found === 0 ? (
                            /* No Interactions Found */
                            <div style={{
                                background: 'linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%)',
                                border: '1px solid #10B981',
                                borderRadius: '24px',
                                padding: '3.5rem 2.5rem',
                                textAlign: 'center'
                            }}>
                                <div style={{
                                    display: 'inline-flex',
                                    padding: '1.25rem',
                                    background: 'linear-gradient(135deg, #10B981 0%, #34D399 100%)',
                                    borderRadius: '50%',
                                    marginBottom: '1.5rem'
                                }}>
                                    <CheckCircle size={48} style={{ color: 'white' }} />
                                </div>
                                <h3 style={{
                                    fontSize: '1.875rem',
                                    fontWeight: 800,
                                    color: '#065F46',
                                    marginBottom: '1rem',
                                    letterSpacing: '-0.01em'
                                }}>
                                    No Known Interactions
                                </h3>
                                <p style={{
                                    fontSize: '1.125rem',
                                    color: '#047857',
                                    maxWidth: '36rem',
                                    margin: '0 auto 1.5rem',
                                    lineHeight: 1.7,
                                    fontWeight: 500
                                }}>
                                    Based on FDA drug labeling, no documented interactions were found between these medications.
                                </p>
                                <p style={{
                                    fontSize: '0.875rem',
                                    color: '#6B7280',
                                    fontStyle: 'italic'
                                }}>
                                    Note: Always consult a healthcare professional for complete information.
                                </p>
                            </div>
                        ) : (
                            /* Interactions Detected */
                            <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
                                {/* Warning Banner */}
                                <div style={{
                                    background: 'linear-gradient(135deg, #FEE2E2 0%, #FECACA 100%)',
                                    border: '2px solid #DC2626',
                                    borderRadius: '20px',
                                    padding: '2rem',
                                    display: 'flex',
                                    alignItems: 'center',
                                    gap: '1.25rem'
                                }}>
                                    <div style={{
                                        padding: '1rem',
                                        background: 'linear-gradient(135deg, #DC2626 0%, #EF4444 100%)',
                                        borderRadius: '16px',
                                        flexShrink: 0
                                    }}>
                                        <AlertTriangle size={32} style={{ color: 'white' }} />
                                    </div>
                                    <div style={{ flex: 1 }}>
                                        <h3 style={{
                                            fontSize: '1.5rem',
                                            fontWeight: 800,
                                            color: '#991B1B',
                                            marginBottom: '0.5rem',
                                            letterSpacing: '-0.01em'
                                        }}>
                                            {interactionResults.interactions_found} Interaction{interactionResults.interactions_found > 1 ? 's' : ''} Detected
                                        </h3>
                                        <p style={{
                                            fontSize: '1rem',
                                            color: '#7F1D1D',
                                            fontWeight: 500
                                        }}>
                                            Review the details below carefully
                                        </p>
                                    </div>
                                </div>

                                {/* Interaction Cards */}
                                {interactionResults.interactions?.map((int, idx) => {
                                    const severityColors = getSeverityColor(int.severity);
                                    return (
                                        <div
                                            key={idx}
                                            style={{
                                                background: 'white',
                                                border: `2px solid ${severityColors.border}`,
                                                borderRadius: '24px',
                                                overflow: 'hidden',
                                                boxShadow: '0 4px 25px -5px rgba(0, 0, 0, 0.1)'
                                            }}
                                        >
                                            {/* Header */}
                                            <div style={{
                                                background: `linear-gradient(135deg, ${severityColors.bg} 0%, ${severityColors.bg}dd 100%)`,
                                                padding: '1.75rem 2rem',
                                                borderBottom: `1px solid ${severityColors.border}`,
                                                display: 'flex',
                                                alignItems: 'center',
                                                justifyContent: 'space-between',
                                                flexWrap: 'wrap',
                                                gap: '1rem'
                                            }}>
                                                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', flex: 1 }}>
                                                    <Zap size={24} style={{ color: severityColors.text }} />
                                                    <span style={{
                                                        fontSize: '1.375rem',
                                                        fontWeight: 700,
                                                        color: '#1F2937'
                                                    }}>
                                                        {int.drug1} <span style={{
                                                            color: severityColors.text,
                                                            margin: '0 0.5rem',
                                                            fontSize: '1.5rem'
                                                        }}>↔</span> {int.drug2}
                                                    </span>
                                                </div>
                                                <span style={{
                                                    padding: '0.625rem 1.25rem',
                                                    borderRadius: '9999px',
                                                    fontSize: '0.9375rem',
                                                    fontWeight: 700,
                                                    background: severityColors.bg,
                                                    color: severityColors.text,
                                                    border: `2px solid ${severityColors.border}`,
                                                    textTransform: 'uppercase',
                                                    letterSpacing: '0.05rem'
                                                }}>
                                                    {int.severity}
                                                </span>
                                            </div>

                                            {/* Content */}
                                            <div style={{ padding: '2.5rem' }}>
                                                <h4 style={{
                                                    fontSize: '1.125rem',
                                                    fontWeight: 700,
                                                    color: '#374151',
                                                    marginBottom: '1.25rem',
                                                    display: 'flex',
                                                    alignItems: 'center',
                                                    gap: '0.5rem'
                                                }}>
                                                    <BookOpen size={20} style={{ color: '#7C3AED' }} />
                                                    Clinical Information:
                                                </h4>
                                                <p style={{
                                                    fontSize: '1.0625rem',
                                                    color: '#4B5563',
                                                    lineHeight: 1.8,
                                                    whiteSpace: 'pre-wrap',
                                                    fontWeight: 500,
                                                    background: '#F9FAFB',
                                                    padding: '1.5rem',
                                                    borderRadius: '16px',
                                                    border: '1px solid #E5E7EB'
                                                }}>
                                                    {int.description}
                                                </p>

                                                {/* Source Footer */}
                                                <div style={{
                                                    marginTop: '2rem',
                                                    paddingTop: '1.5rem',
                                                    borderTop: '1px solid #E5E7EB',
                                                    display: 'flex',
                                                    alignItems: 'center',
                                                    gap: '0.75rem'
                                                }}>
                                                    <div style={{
                                                        padding: '0.5rem',
                                                        background: 'linear-gradient(135deg, #10B981 0%, #34D399 100%)',
                                                        borderRadius: '8px'
                                                    }}>
                                                        <Shield size={16} style={{ color: 'white' }} />
                                                    </div>
                                                    <span style={{
                                                        fontSize: '0.875rem',
                                                        color: '#6B7280',
                                                        fontWeight: 600
                                                    }}>
                                                        Source: <span style={{ color: '#10B981' }}>{int.source}</span>
                                                    </span>
                                                </div>
                                            </div>
                                        </div>
                                    );
                                })}
                            </div>
                        )}

                        {/* Source Attribution */}
                        <p style={{
                            textAlign: 'center',
                            fontSize: '0.875rem',
                            color: '#9CA3AF',
                            fontStyle: 'italic'
                        }}>
                            Source: {interactionResults.source}
                        </p>
                    </motion.div>
                )}

                {/* No Results */}
                {results && !results.drug_found && !results.spelling_suggestion && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        className="bg-white border border-gray-200 rounded-xl p-8 text-center shadow-sm"
                    >
                        <XCircle className="w-12 h-12 text-gray-400 mx-auto mb-3" />
                        <h3 className="text-lg font-semibold text-gray-700">Drug Not Found</h3>
                        <p className="text-gray-500 text-sm mt-1">
                            Please check the spelling or try a different drug name
                        </p>
                    </motion.div>
                )}

                {/* Disclaimer */}
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.3 }}
                    className="bg-yellow-50 border border-yellow-200 rounded-xl p-4"
                >
                    <p className="text-sm text-gray-700 flex items-start gap-2">
                        <AlertTriangle className="w-4 h-4 mt-0.5 shrink-0 text-yellow-600" />
                        <span>
                            <strong>Important:</strong> This information is for research and educational purposes only.
                            Always consult with a qualified healthcare professional before making medical decisions or taking medications.
                            Drug information may change; verify with current prescribing information.
                        </span>
                    </p>
                </motion.div>
            </div>
        </div>
    );
}
