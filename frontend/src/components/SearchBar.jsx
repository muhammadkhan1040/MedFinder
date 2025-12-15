import { useState, useEffect, useRef, useCallback } from 'react';
import { Search, X, Loader2, Pill, FlaskConical, Command } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { getAutocomplete } from '../api/medfinder';
import { debounce } from '../utils/debounce';

/**
 * SearchBar Component - Premium Redesign
 * 
 * Features:
 * - Glassmorphism styling with gradient border focus
 * - Real-time autocomplete (300ms debounce)
 * - Keyboard navigation (Arrow keys + Enter + Escape)
 * - Loading spinner with smooth animation
 * - Premium dropdown with category headers
 * - Keyboard shortcut hint
 */
const SearchBar = ({
    onSearch,
    onSuggestionSelect,
    placeholder = "Search medicines...",
    size = "default" // "default" | "large"
}) => {
    const [query, setQuery] = useState('');
    const [suggestions, setSuggestions] = useState({ medicines: [], compositions: [] });
    const [isLoading, setIsLoading] = useState(false);
    const [showDropdown, setShowDropdown] = useState(false);
    const [selectedIndex, setSelectedIndex] = useState(-1);
    const [isFocused, setIsFocused] = useState(false);

    const inputRef = useRef(null);
    const dropdownRef = useRef(null);

    // Debounced fetch suggestions
    const fetchSuggestions = useCallback(
        debounce(async (searchQuery) => {
            if (searchQuery.length < 2) {
                setSuggestions({ medicines: [], compositions: [] });
                setIsLoading(false);
                return;
            }

            try {
                const result = await getAutocomplete(searchQuery, 10);
                if (result.success) {
                    setSuggestions({
                        medicines: result.medicines || [],
                        compositions: result.compositions || [],
                    });
                }
            } catch (error) {
                console.error('Autocomplete error:', error);
            } finally {
                setIsLoading(false);
            }
        }, 300),
        []
    );

    // Handle input change
    const handleInputChange = (e) => {
        const value = e.target.value;
        setQuery(value);
        setSelectedIndex(-1);

        if (value.length >= 2) {
            setIsLoading(true);
            setShowDropdown(true);
            fetchSuggestions(value);
        } else {
            setShowDropdown(false);
            setSuggestions({ medicines: [], compositions: [] });
        }
    };

    // Get all suggestions as flat array
    const getAllSuggestions = () => {
        const all = [];
        suggestions.medicines.forEach((med, i) => {
            all.push({ type: 'medicine', value: med, index: i });
        });
        suggestions.compositions.forEach((comp, i) => {
            all.push({ type: 'composition', value: comp, index: suggestions.medicines.length + i });
        });
        return all;
    };

    // Handle keyboard navigation
    const handleKeyDown = (e) => {
        const allSuggestions = getAllSuggestions();

        switch (e.key) {
            case 'ArrowDown':
                e.preventDefault();
                setSelectedIndex(prev =>
                    prev < allSuggestions.length - 1 ? prev + 1 : prev
                );
                break;
            case 'ArrowUp':
                e.preventDefault();
                setSelectedIndex(prev => prev > 0 ? prev - 1 : -1);
                break;
            case 'Enter':
                e.preventDefault();
                if (selectedIndex >= 0 && selectedIndex < allSuggestions.length) {
                    handleSuggestionClick(allSuggestions[selectedIndex]);
                } else if (query.trim()) {
                    handleSearch();
                }
                break;
            case 'Escape':
                setShowDropdown(false);
                setSelectedIndex(-1);
                inputRef.current?.blur();
                break;
            default:
                break;
        }
    };

    // Handle suggestion click
    const handleSuggestionClick = (suggestion) => {
        setQuery(suggestion.value);
        setShowDropdown(false);
        setSelectedIndex(-1);

        if (onSuggestionSelect) {
            onSuggestionSelect(suggestion);
        } else if (onSearch) {
            onSearch(suggestion.value);
        }
    };

    // Handle search submit
    const handleSearch = () => {
        if (query.trim() && onSearch) {
            onSearch(query.trim());
            setShowDropdown(false);
        }
    };

    // Clear input
    const handleClear = () => {
        setQuery('');
        setSuggestions({ medicines: [], compositions: [] });
        setShowDropdown(false);
        setSelectedIndex(-1);
        inputRef.current?.focus();
    };

    // Close dropdown when clicking outside
    useEffect(() => {
        const handleClickOutside = (e) => {
            if (
                dropdownRef.current &&
                !dropdownRef.current.contains(e.target) &&
                !inputRef.current?.contains(e.target)
            ) {
                setShowDropdown(false);
            }
        };

        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    // Keyboard shortcut (Ctrl+K / Cmd+K)
    useEffect(() => {
        const handleKeyboard = (e) => {
            if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
                e.preventDefault();
                inputRef.current?.focus();
            }
        };

        document.addEventListener('keydown', handleKeyboard);
        return () => document.removeEventListener('keydown', handleKeyboard);
    }, []);

    const isLarge = size === 'large';
    const allSuggestions = getAllSuggestions();
    const hasSuggestions = allSuggestions.length > 0;

    return (
        <div style={{ position: 'relative', width: '100%' }}>
            {/* Search Input Container */}
            <motion.div
                animate={{
                    boxShadow: isFocused
                        ? '0 0 0 4px rgba(59, 130, 246, 0.15), 0 20px 40px -10px rgba(0, 0, 0, 0.15)'
                        : '0 4px 20px -5px rgba(0, 0, 0, 0.1)',
                }}
                style={{
                    position: 'relative',
                    background: 'white',
                    borderRadius: isLarge ? '16px' : '12px',
                    border: isFocused
                        ? '2px solid #3B82F6'
                        : '2px solid transparent',
                    transition: 'border-color 0.2s ease',
                    overflow: 'hidden',
                }}
            >
                {/* Gradient Border Effect */}
                {isFocused && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        style={{
                            position: 'absolute',
                            inset: '-2px',
                            borderRadius: isLarge ? '18px' : '14px',
                            padding: '2px',
                            background: 'linear-gradient(135deg, #3B82F6 0%, #8B5CF6 50%, #EC4899 100%)',
                            WebkitMask: 'linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0)',
                            WebkitMaskComposite: 'xor',
                            maskComposite: 'exclude',
                            pointerEvents: 'none',
                            zIndex: 0,
                        }}
                    />
                )}

                {/* Search Icon */}
                <div style={{
                    position: 'absolute',
                    left: isLarge ? '1.25rem' : '1rem',
                    top: '50%',
                    transform: 'translateY(-50%)',
                    color: isFocused ? '#3B82F6' : '#94A3B8',
                    transition: 'color 0.2s ease',
                    zIndex: 1,
                }}>
                    <Search size={isLarge ? 24 : 20} />
                </div>

                {/* Input */}
                <input
                    ref={inputRef}
                    type="text"
                    value={query}
                    onChange={handleInputChange}
                    onKeyDown={handleKeyDown}
                    onFocus={() => {
                        setIsFocused(true);
                        if (query.length >= 2 && hasSuggestions) {
                            setShowDropdown(true);
                        }
                    }}
                    onBlur={() => setIsFocused(false)}
                    placeholder={placeholder}
                    style={{
                        width: '100%',
                        padding: isLarge ? '1.125rem 1.5rem' : '0.875rem 1.25rem',
                        paddingLeft: isLarge ? '3.5rem' : '3rem',
                        paddingRight: isLarge ? '8rem' : '7rem',
                        fontSize: isLarge ? '1.125rem' : '1rem',
                        border: 'none',
                        outline: 'none',
                        background: 'transparent',
                        color: '#1E293B',
                        fontFamily: 'inherit',
                        position: 'relative',
                        zIndex: 1,
                    }}
                    aria-label="Search medicines"
                    aria-autocomplete="list"
                    aria-expanded={showDropdown}
                />

                {/* Right Side Actions */}
                <div style={{
                    position: 'absolute',
                    right: isLarge ? '0.75rem' : '0.5rem',
                    top: '50%',
                    transform: 'translateY(-50%)',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.5rem',
                    zIndex: 1,
                }}>
                    {/* Keyboard Shortcut Hint */}
                    {!query && !isFocused && (
                        <div style={{
                            display: 'flex',
                            alignItems: 'center',
                            gap: '0.25rem',
                            padding: '0.25rem 0.5rem',
                            background: '#F1F5F9',
                            borderRadius: '6px',
                            color: '#94A3B8',
                            fontSize: '0.75rem',
                            fontWeight: 500,
                        }}>
                            <Command size={12} />
                            <span>K</span>
                        </div>
                    )}

                    {/* Loading Spinner */}
                    {isLoading && (
                        <motion.div
                            animate={{ rotate: 360 }}
                            transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
                        >
                            <Loader2 size={20} style={{ color: '#3B82F6' }} />
                        </motion.div>
                    )}

                    {/* Clear Button */}
                    {query && !isLoading && (
                        <motion.button
                            whileHover={{ scale: 1.1 }}
                            whileTap={{ scale: 0.9 }}
                            onClick={handleClear}
                            style={{
                                padding: '0.375rem',
                                background: '#F1F5F9',
                                border: 'none',
                                borderRadius: '8px',
                                color: '#64748B',
                                cursor: 'pointer',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                            }}
                            aria-label="Clear search"
                        >
                            <X size={16} />
                        </motion.button>
                    )}

                    {/* Search Button */}
                    <motion.button
                        whileHover={{ scale: 1.05, boxShadow: '0 4px 15px rgba(59, 130, 246, 0.4)' }}
                        whileTap={{ scale: 0.95 }}
                        onClick={handleSearch}
                        style={{
                            padding: isLarge ? '0.625rem 1rem' : '0.5rem 0.875rem',
                            background: 'linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%)',
                            border: 'none',
                            borderRadius: isLarge ? '12px' : '8px',
                            color: 'white',
                            cursor: 'pointer',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            boxShadow: '0 2px 10px rgba(59, 130, 246, 0.3)',
                        }}
                        aria-label="Search"
                    >
                        <Search size={isLarge ? 20 : 18} />
                    </motion.button>
                </div>
            </motion.div>

            {/* Autocomplete Dropdown */}
            <AnimatePresence>
                {showDropdown && (hasSuggestions || isLoading) && (
                    <motion.div
                        ref={dropdownRef}
                        initial={{ opacity: 0, y: -10, scale: 0.98 }}
                        animate={{ opacity: 1, y: 0, scale: 1 }}
                        exit={{ opacity: 0, y: -10, scale: 0.98 }}
                        transition={{ duration: 0.2, ease: 'easeOut' }}
                        style={{
                            position: 'absolute',
                            zIndex: 100,
                            width: '100%',
                            marginTop: '0.75rem',
                            background: 'rgba(255, 255, 255, 0.95)',
                            backdropFilter: 'blur(20px)',
                            WebkitBackdropFilter: 'blur(20px)',
                            borderRadius: '16px',
                            boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.2)',
                            border: '1px solid rgba(255, 255, 255, 0.5)',
                            overflow: 'hidden',
                        }}
                    >
                        {isLoading && !hasSuggestions ? (
                            <div style={{
                                padding: '2rem',
                                textAlign: 'center',
                                color: '#64748B',
                            }}>
                                <motion.div
                                    animate={{ rotate: 360 }}
                                    transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
                                    style={{ display: 'inline-block', marginBottom: '0.5rem' }}
                                >
                                    <Loader2 size={24} style={{ color: '#3B82F6' }} />
                                </motion.div>
                                <p style={{ fontSize: '0.875rem' }}>Searching...</p>
                            </div>
                        ) : (
                            <ul style={{
                                maxHeight: '24rem',
                                overflowY: 'auto',
                                margin: 0,
                                padding: 0,
                                listStyle: 'none',
                            }}>
                                {/* Medicine Suggestions */}
                                {suggestions.medicines.length > 0 && (
                                    <>
                                        <li style={{
                                            padding: '0.75rem 1rem',
                                            fontSize: '0.6875rem',
                                            fontWeight: 600,
                                            color: '#94A3B8',
                                            textTransform: 'uppercase',
                                            letterSpacing: '0.05em',
                                            background: '#F8FAFC',
                                            borderBottom: '1px solid #E2E8F0',
                                        }}>
                                            Medicines
                                        </li>
                                        {suggestions.medicines.map((med, index) => (
                                            <motion.li
                                                key={`med-${index}`}
                                                whileHover={{ background: 'rgba(59, 130, 246, 0.05)' }}
                                                onClick={() => handleSuggestionClick({ type: 'medicine', value: med })}
                                                style={{
                                                    padding: '0.875rem 1rem',
                                                    cursor: 'pointer',
                                                    display: 'flex',
                                                    alignItems: 'center',
                                                    gap: '0.75rem',
                                                    borderBottom: '1px solid #F1F5F9',
                                                    background: selectedIndex === index
                                                        ? 'rgba(59, 130, 246, 0.08)'
                                                        : 'transparent',
                                                    transition: 'background 0.15s ease',
                                                }}
                                            >
                                                <div style={{
                                                    padding: '0.5rem',
                                                    background: 'rgba(59, 130, 246, 0.1)',
                                                    borderRadius: '8px',
                                                }}>
                                                    <Pill size={16} style={{ color: '#3B82F6' }} />
                                                </div>
                                                <span style={{
                                                    fontWeight: 500,
                                                    color: selectedIndex === index ? '#3B82F6' : '#1E293B',
                                                }}>
                                                    {med}
                                                </span>
                                            </motion.li>
                                        ))}
                                    </>
                                )}

                                {/* Composition Suggestions */}
                                {suggestions.compositions.length > 0 && (
                                    <>
                                        <li style={{
                                            padding: '0.75rem 1rem',
                                            fontSize: '0.6875rem',
                                            fontWeight: 600,
                                            color: '#94A3B8',
                                            textTransform: 'uppercase',
                                            letterSpacing: '0.05em',
                                            background: '#F8FAFC',
                                            borderBottom: '1px solid #E2E8F0',
                                        }}>
                                            Formulas / Compositions
                                        </li>
                                        {suggestions.compositions.map((comp, index) => {
                                            const actualIndex = suggestions.medicines.length + index;
                                            return (
                                                <motion.li
                                                    key={`comp-${index}`}
                                                    whileHover={{ background: 'rgba(139, 92, 246, 0.05)' }}
                                                    onClick={() => handleSuggestionClick({ type: 'composition', value: comp })}
                                                    style={{
                                                        padding: '0.875rem 1rem',
                                                        cursor: 'pointer',
                                                        display: 'flex',
                                                        alignItems: 'center',
                                                        gap: '0.75rem',
                                                        borderBottom: '1px solid #F1F5F9',
                                                        background: selectedIndex === actualIndex
                                                            ? 'rgba(139, 92, 246, 0.08)'
                                                            : 'transparent',
                                                        transition: 'background 0.15s ease',
                                                    }}
                                                >
                                                    <div style={{
                                                        padding: '0.5rem',
                                                        background: 'rgba(139, 92, 246, 0.1)',
                                                        borderRadius: '8px',
                                                    }}>
                                                        <FlaskConical size={16} style={{ color: '#8B5CF6' }} />
                                                    </div>
                                                    <div>
                                                        <span style={{
                                                            fontWeight: 500,
                                                            color: selectedIndex === actualIndex ? '#8B5CF6' : '#1E293B',
                                                        }}>
                                                            {comp}
                                                        </span>
                                                        <span style={{
                                                            fontSize: '0.75rem',
                                                            color: '#94A3B8',
                                                            marginLeft: '0.5rem',
                                                        }}>
                                                            Formula search
                                                        </span>
                                                    </div>
                                                </motion.li>
                                            );
                                        })}
                                    </>
                                )}
                            </ul>
                        )}
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
};

export default SearchBar;
