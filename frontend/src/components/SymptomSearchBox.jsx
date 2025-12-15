import React, { useState } from 'react';
import { Search, Loader2, AlertCircle } from 'lucide-react';

const SymptomSearchBox = ({ onSearch, isLoading }) => {
    const [query, setQuery] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();

        if (!query.trim()) {
            setError('Please describe your symptoms');
            return;
        }

        if (query.trim().length < 5) {
            setError('Please provide more detail about your symptoms');
            return;
        }

        setError('');
        onSearch(query);
    };

    return (
        <div className="w-full max-w-3xl mx-auto">
            <form onSubmit={handleSubmit} className="relative">
                <div className="relative group">
                    <div className="absolute inset-0 bg-blue-500 rounded-2xl blur opacity-20 group-hover:opacity-30 transition duration-1000"></div>

                    <div className="relative bg-white rounded-2xl shadow-xl transition-shadow hover:shadow-2xl overflow-hidden border border-gray-100 p-2">
                        <textarea
                            value={query}
                            onChange={(e) => {
                                setQuery(e.target.value);
                                if (error) setError('');
                            }}
                            placeholder="Describe your symptoms in detail (e.g., 'I have a severe headache and fever with nausea')..."
                            className="w-full p-4 text-lg text-gray-700 placeholder-gray-400 bg-transparent border-none outline-none resize-none min-h-[120px]"
                            disabled={isLoading}
                        />

                        <div className="flex justify-between items-center px-4 pb-2">
                            <span className={`text-sm ${query.length > 500 ? 'text-red-500' : 'text-gray-400'}`}>
                                {query.length}/500 characters
                            </span>

                            <button
                                type="submit"
                                disabled={isLoading || !query.trim()}
                                className={`flex items-center gap-2 px-6 py-3 rounded-xl font-semibold text-white transition-all duration-300
                  ${isLoading || !query.trim()
                                        ? 'bg-gray-300 cursor-not-allowed'
                                        : 'bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 shadow-md hover:shadow-lg transform hover:-translate-y-0.5'
                                    }`}
                            >
                                {isLoading ? (
                                    <>
                                        <Loader2 size={20} className="animate-spin" />
                                        Analyzing...
                                    </>
                                ) : (
                                    <>
                                        <Search size={20} />
                                        Analyze Symptoms
                                    </>
                                )}
                            </button>
                        </div>
                    </div>
                </div>
            </form>

            {error && (
                <div className="flex items-center gap-2 mt-3 text-red-500 bg-red-50 px-4 py-2 rounded-lg text-sm animate-fade-in">
                    <AlertCircle size={16} />
                    {error}
                </div>
            )}

            <div className="mt-8 flex flex-wrap gap-2 justify-center text-sm text-gray-500">
                <span>Try:</span>
                <button
                    onClick={() => setQuery("Splitting headache and sensitivity to light")}
                    className="px-3 py-1 bg-white border border-gray-200 rounded-full hover:border-blue-300 hover:text-blue-600 transition-colors"
                >
                    "Splitting headache..."
                </button>
                <button
                    onClick={() => setQuery("High fever with chills and body aches")}
                    className="px-3 py-1 bg-white border border-gray-200 rounded-full hover:border-blue-300 hover:text-blue-600 transition-colors"
                >
                    "High fever..."
                </button>
                <button
                    onClick={() => setQuery("Stomach pain and nausea after eating")}
                    className="px-3 py-1 bg-white border border-gray-200 rounded-full hover:border-blue-300 hover:text-blue-600 transition-colors"
                >
                    "Stomach pain..."
                </button>
            </div>
        </div>
    );
};

export default SymptomSearchBox;
