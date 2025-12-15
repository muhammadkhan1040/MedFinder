import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    X, Pill, Building2, FlaskConical, CheckCircle, TrendingDown, ExternalLink,
    Package, Loader2, Info, AlertTriangle, ShieldAlert, HelpCircle, Stethoscope,
    ChevronDown, ChevronUp, Activity
} from 'lucide-react';
import { getSimilarMedicines, checkAvailability } from '../api/medfinder';

/**
 * DetailModal Component - Full Information View
 * 
 * Large modal with comprehensive medicine information including:
 * - Introduction, Primary Uses, Side Effects
 * - Warnings, Contraindications, FAQs, Expert Advice
 * - Alternatives and Availability
 */
const DetailModal = ({
    medicine,
    isOpen,
    onClose,
    onSelectAlternative
}) => {
    const [activeSection, setActiveSection] = useState('overview');
    const [alternatives, setAlternatives] = useState([]);
    const [isLoadingAlternatives, setIsLoadingAlternatives] = useState(false);
    const [availability, setAvailability] = useState(null);
    const [isCheckingAvailability, setIsCheckingAvailability] = useState(false);
    const [expandedFaq, setExpandedFaq] = useState(null);

    useEffect(() => {
        if (isOpen && medicine) {
            setActiveSection('overview');
            setAvailability(null);
            setExpandedFaq(null);
            loadAlternatives();
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = 'unset';
        }
        return () => { document.body.style.overflow = 'unset'; };
    }, [isOpen, medicine]);

    const loadAlternatives = async () => {
        if (!medicine?.name) return;
        setIsLoadingAlternatives(true);
        try {
            const result = await getSimilarMedicines(medicine.name, 5);
            if (result.success) setAlternatives(result.alternatives || []);
        } catch (error) {
            console.error('Failed to load alternatives:', error);
        } finally {
            setIsLoadingAlternatives(false);
        }
    };

    const handleCheckAvailability = async () => {
        if (!medicine?.name) return;
        setIsCheckingAvailability(true);
        try {
            const result = await checkAvailability(medicine.name);
            setAvailability(result.available);
        } catch (error) {
            setAvailability(-1);
        } finally {
            setIsCheckingAvailability(false);
        }
    };

    const formatPrice = (priceStr) => {
        if (!priceStr || priceStr === 'N/A') return 'Price not available';
        if (typeof priceStr === 'string' && priceStr.includes('Rs.')) return priceStr;
        const num = parseFloat(String(priceStr).replace(/[^0-9.]/g, ''));
        return isNaN(num) ? 'Price not available' : `Rs. ${num.toFixed(2)}`;
    };

    if (!medicine) return null;

    // Extract all medicine data
    const name = medicine.name || 'Unknown Medicine';
    const brand = medicine.brand || 'Unknown Brand';
    const price = formatPrice(medicine.price);
    const composition = medicine.composition || '';
    const categories = medicine.categories || [];
    const packSize = medicine.pack_size || medicine.packSize || '';
    const introduction = medicine.introduction || '';
    const primaryUses = medicine.primary_uses || '';
    const sideEffects = medicine.side_effects || '';
    const warnings = medicine.warnings || '';
    const contraindications = medicine.contraindications || '';
    const faqs = medicine.faqs || [];
    const expertAdvice = medicine.expert_advice || '';
    const indications = medicine.indications || '';

    const sections = [
        { id: 'overview', label: 'Overview', icon: Info },
        { id: 'uses', label: 'Uses & Effects', icon: Activity },
        { id: 'safety', label: 'Safety Info', icon: ShieldAlert },
        { id: 'alternatives', label: 'Alternatives', icon: TrendingDown },
    ];

    // Section Card Component
    const InfoCard = ({ icon: Icon, title, content, color = '#3B82F6', bgColor = 'rgba(59, 130, 246, 0.08)' }) => {
        if (!content) return null;
        return (
            <div style={{
                background: 'white',
                borderRadius: '16px',
                border: '1px solid #E5E7EB',
                overflow: 'hidden',
                marginBottom: '1rem',
            }}>
                <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.75rem',
                    padding: '1rem 1.25rem',
                    background: bgColor,
                    borderBottom: '1px solid #E5E7EB',
                }}>
                    <Icon size={20} style={{ color, flexShrink: 0 }} />
                    <h3 style={{ fontWeight: 700, color: '#1F2937', fontSize: '1rem', margin: 0 }}>{title}</h3>
                </div>
                <div style={{ padding: '1rem 1.25rem' }}>
                    <p style={{ color: '#4B5563', fontSize: '0.9375rem', lineHeight: 1.7, whiteSpace: 'pre-wrap', margin: 0 }}>
                        {content}
                    </p>
                </div>
            </div>
        );
    };

    return (
        <AnimatePresence>
            {isOpen && (
                <div style={{
                    position: 'fixed',
                    top: 0, left: 0, right: 0, bottom: 0,
                    zIndex: 9999,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    padding: '1rem',
                }}>
                    {/* Backdrop */}
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        onClick={onClose}
                        style={{
                            position: 'absolute',
                            inset: 0,
                            background: 'rgba(0, 0, 0, 0.75)',
                            backdropFilter: 'blur(8px)',
                        }}
                    />

                    {/* Modal - LARGER SIZE */}
                    <motion.div
                        initial={{ opacity: 0, scale: 0.95, y: 20 }}
                        animate={{ opacity: 1, scale: 1, y: 0 }}
                        exit={{ opacity: 0, scale: 0.95, y: 20 }}
                        transition={{ type: 'spring', damping: 25, stiffness: 300 }}
                        style={{
                            position: 'relative',
                            width: '100%',
                            maxWidth: '900px',
                            height: '90vh',
                            maxHeight: '800px',
                            background: '#F9FAFB',
                            borderRadius: '24px',
                            boxShadow: '0 25px 80px -20px rgba(0, 0, 0, 0.5)',
                            display: 'flex',
                            flexDirection: 'column',
                            overflow: 'hidden',
                        }}
                    >
                        {/* Header */}
                        <div style={{
                            background: 'linear-gradient(135deg, #1E40AF 0%, #7C3AED 100%)',
                            padding: '1.5rem 2rem',
                            color: 'white',
                            flexShrink: 0,
                        }}>
                            {/* Close Button */}
                            <button
                                onClick={onClose}
                                style={{
                                    position: 'absolute',
                                    top: '1rem',
                                    right: '1rem',
                                    padding: '0.5rem',
                                    background: 'rgba(255, 255, 255, 0.2)',
                                    border: 'none',
                                    borderRadius: '10px',
                                    color: 'white',
                                    cursor: 'pointer',
                                    display: 'flex',
                                }}
                            >
                                <X size={20} />
                            </button>

                            <div style={{ display: 'flex', alignItems: 'flex-start', gap: '1rem' }}>
                                <div style={{
                                    padding: '1rem',
                                    background: 'rgba(255, 255, 255, 0.2)',
                                    borderRadius: '16px',
                                    flexShrink: 0,
                                }}>
                                    <Pill size={32} />
                                </div>
                                <div style={{ flex: 1, paddingRight: '2.5rem' }}>
                                    <h1 style={{ fontSize: '1.5rem', fontWeight: 800, marginBottom: '0.375rem', lineHeight: 1.2 }}>
                                        {name}
                                    </h1>
                                    <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', flexWrap: 'wrap', opacity: 0.9, fontSize: '0.9rem' }}>
                                        <span style={{ display: 'flex', alignItems: 'center', gap: '0.375rem' }}>
                                            <Building2 size={14} /> {brand}
                                        </span>
                                        {packSize && (
                                            <span style={{ display: 'flex', alignItems: 'center', gap: '0.375rem' }}>
                                                <Package size={14} /> {packSize}
                                            </span>
                                        )}
                                    </div>
                                </div>
                            </div>

                            {/* Price and Availability */}
                            <div style={{ marginTop: '1.25rem', display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1rem' }}>
                                <div>
                                    <p style={{ fontSize: '0.75rem', opacity: 0.7, marginBottom: '0.25rem' }}>Price</p>
                                    <p style={{ fontSize: '2rem', fontWeight: 800, fontFamily: "'JetBrains Mono', monospace" }}>{price}</p>
                                </div>
                                <div style={{ display: 'flex', gap: '0.75rem' }}>
                                    <button
                                        onClick={handleCheckAvailability}
                                        disabled={isCheckingAvailability}
                                        style={{
                                            padding: '0.625rem 1.25rem',
                                            background: availability === 1 ? '#10B981' : availability === 0 ? '#EF4444' : 'rgba(255,255,255,0.2)',
                                            border: 'none',
                                            borderRadius: '10px',
                                            color: 'white',
                                            fontWeight: 600,
                                            fontSize: '0.875rem',
                                            cursor: 'pointer',
                                            display: 'flex',
                                            alignItems: 'center',
                                            gap: '0.5rem',
                                        }}
                                    >
                                        {isCheckingAvailability ? (
                                            <><Loader2 size={16} style={{ animation: 'spin 1s linear infinite' }} /> Checking...</>
                                        ) : availability === 1 ? (
                                            <><CheckCircle size={16} /> In Stock</>
                                        ) : availability === 0 ? (
                                            <><X size={16} /> Out of Stock</>
                                        ) : (
                                            <><CheckCircle size={16} /> Check Stock</>
                                        )}
                                    </button>
                                    <a
                                        href={`https://dawaai.pk/search?q=${encodeURIComponent(name)}`}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        style={{
                                            padding: '0.625rem 1.25rem',
                                            background: 'white',
                                            color: '#1E40AF',
                                            border: 'none',
                                            borderRadius: '10px',
                                            fontWeight: 600,
                                            fontSize: '0.875rem',
                                            textDecoration: 'none',
                                            display: 'flex',
                                            alignItems: 'center',
                                            gap: '0.5rem',
                                        }}
                                    >
                                        <ExternalLink size={16} /> Buy Now
                                    </a>
                                </div>
                            </div>
                        </div>

                        {/* Navigation Tabs */}
                        <div style={{
                            display: 'flex',
                            background: 'white',
                            borderBottom: '1px solid #E5E7EB',
                            padding: '0 1rem',
                            overflowX: 'auto',
                            flexShrink: 0,
                        }}>
                            {sections.map((section) => (
                                <button
                                    key={section.id}
                                    onClick={() => setActiveSection(section.id)}
                                    style={{
                                        padding: '1rem 1.25rem',
                                        display: 'flex',
                                        alignItems: 'center',
                                        gap: '0.5rem',
                                        background: 'transparent',
                                        border: 'none',
                                        borderBottom: activeSection === section.id ? '3px solid #3B82F6' : '3px solid transparent',
                                        color: activeSection === section.id ? '#3B82F6' : '#6B7280',
                                        fontWeight: 600,
                                        fontSize: '0.875rem',
                                        cursor: 'pointer',
                                        transition: 'all 0.2s ease',
                                        whiteSpace: 'nowrap',
                                    }}
                                >
                                    <section.icon size={18} />
                                    {section.label}
                                    {section.id === 'alternatives' && alternatives.length > 0 && (
                                        <span style={{
                                            padding: '0.125rem 0.5rem',
                                            background: '#F59E0B',
                                            color: 'white',
                                            borderRadius: '9999px',
                                            fontSize: '0.6875rem',
                                            fontWeight: 700,
                                        }}>
                                            {alternatives.length}
                                        </span>
                                    )}
                                </button>
                            ))}
                        </div>

                        {/* Content Area */}
                        <div style={{
                            flex: 1,
                            overflowY: 'auto',
                            padding: '1.5rem 2rem',
                        }}>
                            {/* Overview Section */}
                            {activeSection === 'overview' && (
                                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                                    {/* Introduction */}
                                    <InfoCard
                                        icon={Info}
                                        title="Introduction"
                                        content={introduction || 'No introduction available for this medicine.'}
                                        color="#3B82F6"
                                        bgColor="rgba(59, 130, 246, 0.08)"
                                    />

                                    {/* Composition */}
                                    <InfoCard
                                        icon={FlaskConical}
                                        title="Composition / Formula"
                                        content={composition || 'Composition not available.'}
                                        color="#8B5CF6"
                                        bgColor="rgba(139, 92, 246, 0.08)"
                                    />

                                    {/* Categories */}
                                    {categories.length > 0 && (
                                        <div style={{ marginBottom: '1rem' }}>
                                            <p style={{ fontSize: '0.75rem', color: '#6B7280', fontWeight: 600, textTransform: 'uppercase', marginBottom: '0.5rem' }}>Categories</p>
                                            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                                                {categories.map((cat, i) => (
                                                    <span key={i} style={{
                                                        padding: '0.375rem 0.875rem',
                                                        background: 'rgba(59, 130, 246, 0.1)',
                                                        color: '#3B82F6',
                                                        borderRadius: '9999px',
                                                        fontSize: '0.8125rem',
                                                        fontWeight: 500,
                                                    }}>
                                                        {cat}
                                                    </span>
                                                ))}
                                            </div>
                                        </div>
                                    )}

                                    {/* Expert Advice */}
                                    <InfoCard
                                        icon={Stethoscope}
                                        title="Expert Advice"
                                        content={expertAdvice}
                                        color="#10B981"
                                        bgColor="rgba(16, 185, 129, 0.08)"
                                    />
                                </motion.div>
                            )}

                            {/* Uses & Effects Section */}
                            {activeSection === 'uses' && (
                                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                                    <InfoCard
                                        icon={Activity}
                                        title="Primary Uses"
                                        content={primaryUses || indications || 'No usage information available.'}
                                        color="#10B981"
                                        bgColor="rgba(16, 185, 129, 0.08)"
                                    />

                                    <InfoCard
                                        icon={AlertTriangle}
                                        title="Side Effects"
                                        content={sideEffects}
                                        color="#F59E0B"
                                        bgColor="rgba(245, 158, 11, 0.08)"
                                    />

                                    {/* FAQs */}
                                    {faqs && faqs.length > 0 && (
                                        <div style={{
                                            background: 'white',
                                            borderRadius: '16px',
                                            border: '1px solid #E5E7EB',
                                            overflow: 'hidden',
                                        }}>
                                            <div style={{
                                                display: 'flex',
                                                alignItems: 'center',
                                                gap: '0.75rem',
                                                padding: '1rem 1.25rem',
                                                background: 'rgba(139, 92, 246, 0.08)',
                                                borderBottom: '1px solid #E5E7EB',
                                            }}>
                                                <HelpCircle size={20} style={{ color: '#8B5CF6' }} />
                                                <h3 style={{ fontWeight: 700, color: '#1F2937', fontSize: '1rem', margin: 0 }}>
                                                    Frequently Asked Questions
                                                </h3>
                                            </div>
                                            <div style={{ padding: '0.5rem' }}>
                                                {faqs.map((faq, i) => (
                                                    <div key={i} style={{ borderBottom: i < faqs.length - 1 ? '1px solid #E5E7EB' : 'none' }}>
                                                        <button
                                                            onClick={() => setExpandedFaq(expandedFaq === i ? null : i)}
                                                            style={{
                                                                width: '100%',
                                                                padding: '1rem',
                                                                display: 'flex',
                                                                alignItems: 'center',
                                                                justifyContent: 'space-between',
                                                                background: 'transparent',
                                                                border: 'none',
                                                                cursor: 'pointer',
                                                                textAlign: 'left',
                                                            }}
                                                        >
                                                            <span style={{ fontWeight: 600, color: '#1F2937', fontSize: '0.9375rem' }}>
                                                                {faq.question || faq.q}
                                                            </span>
                                                            {expandedFaq === i ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
                                                        </button>
                                                        {expandedFaq === i && (
                                                            <div style={{ padding: '0 1rem 1rem', color: '#4B5563', fontSize: '0.9rem', lineHeight: 1.6 }}>
                                                                {faq.answer || faq.a}
                                                            </div>
                                                        )}
                                                    </div>
                                                ))}
                                            </div>
                                        </div>
                                    )}
                                </motion.div>
                            )}

                            {/* Safety Info Section */}
                            {activeSection === 'safety' && (
                                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                                    <InfoCard
                                        icon={AlertTriangle}
                                        title="Warnings"
                                        content={warnings}
                                        color="#EF4444"
                                        bgColor="rgba(239, 68, 68, 0.08)"
                                    />

                                    <InfoCard
                                        icon={ShieldAlert}
                                        title="Contraindications"
                                        content={contraindications}
                                        color="#DC2626"
                                        bgColor="rgba(220, 38, 38, 0.08)"
                                    />

                                    {/* Safety Notice */}
                                    <div style={{
                                        padding: '1rem',
                                        background: 'rgba(251, 191, 36, 0.1)',
                                        border: '1px solid rgba(251, 191, 36, 0.3)',
                                        borderRadius: '12px',
                                        marginTop: '1rem',
                                    }}>
                                        <p style={{ color: '#92400E', fontSize: '0.875rem', lineHeight: 1.6, margin: 0 }}>
                                            <strong>Important:</strong> Always consult a healthcare professional before taking any medication.
                                            This information is for educational purposes only.
                                        </p>
                                    </div>
                                </motion.div>
                            )}

                            {/* Alternatives Section */}
                            {activeSection === 'alternatives' && (
                                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                                    {isLoadingAlternatives ? (
                                        <div style={{ textAlign: 'center', padding: '3rem' }}>
                                            <Loader2 size={32} style={{ color: '#3B82F6', animation: 'spin 1s linear infinite' }} />
                                            <p style={{ color: '#6B7280', marginTop: '1rem' }}>Finding cheaper alternatives...</p>
                                        </div>
                                    ) : alternatives.length > 0 ? (
                                        <>
                                            <p style={{ color: '#4B5563', marginBottom: '1.5rem', fontSize: '1rem' }}>
                                                Found <strong style={{ color: '#10B981' }}>{alternatives.length}</strong> cheaper alternatives with the same composition:
                                            </p>
                                            <div style={{ display: 'grid', gap: '1rem' }}>
                                                {alternatives.map((alt, index) => (
                                                    <motion.div
                                                        key={index}
                                                        initial={{ opacity: 0, x: -20 }}
                                                        animate={{ opacity: 1, x: 0 }}
                                                        transition={{ delay: index * 0.1 }}
                                                        style={{
                                                            padding: '1.25rem',
                                                            background: 'white',
                                                            border: '1px solid #E5E7EB',
                                                            borderRadius: '16px',
                                                            display: 'flex',
                                                            alignItems: 'center',
                                                            justifyContent: 'space-between',
                                                            transition: 'all 0.2s ease',
                                                        }}
                                                    >
                                                        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                                                            <div style={{
                                                                width: '40px', height: '40px',
                                                                background: 'linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%)',
                                                                borderRadius: '50%',
                                                                display: 'flex', alignItems: 'center', justifyContent: 'center',
                                                                color: 'white', fontWeight: 700, fontSize: '1rem',
                                                            }}>
                                                                {index + 1}
                                                            </div>
                                                            <div>
                                                                <h4 style={{ fontWeight: 700, color: '#1F2937', fontSize: '1rem', marginBottom: '0.25rem' }}>{alt.name}</h4>
                                                                <p style={{ fontSize: '0.875rem', color: '#6B7280' }}>{alt.brand}</p>
                                                            </div>
                                                        </div>
                                                        <div style={{ textAlign: 'right' }}>
                                                            <p style={{ fontWeight: 700, color: '#1F2937', fontSize: '1.125rem', fontFamily: "'JetBrains Mono', monospace" }}>
                                                                {formatPrice(alt.price)}
                                                            </p>
                                                            {alt.savings_percent > 0 && (
                                                                <span style={{
                                                                    display: 'inline-block',
                                                                    padding: '0.25rem 0.75rem',
                                                                    background: 'linear-gradient(135deg, #10B981 0%, #34D399 100%)',
                                                                    color: 'white',
                                                                    borderRadius: '9999px',
                                                                    fontSize: '0.75rem',
                                                                    fontWeight: 700,
                                                                    marginTop: '0.375rem',
                                                                }}>
                                                                    Save {alt.savings_percent.toFixed(0)}%
                                                                </span>
                                                            )}
                                                        </div>
                                                    </motion.div>
                                                ))}
                                            </div>
                                        </>
                                    ) : (
                                        <div style={{ textAlign: 'center', padding: '3rem' }}>
                                            <TrendingDown size={48} style={{ color: '#D1D5DB', marginBottom: '1rem' }} />
                                            <h3 style={{ fontWeight: 600, color: '#4B5563', marginBottom: '0.5rem' }}>No Cheaper Alternatives Found</h3>
                                            <p style={{ color: '#9CA3AF' }}>This might already be the most affordable option.</p>
                                        </div>
                                    )}
                                </motion.div>
                            )}
                        </div>
                    </motion.div>

                    <style>{`@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }`}</style>
                </div>
            )}
        </AnimatePresence>
    );
};

export default DetailModal;
