#!/usr/bin/env python3
"""
Vulnerability Pattern Analysis Tool for Claude 3.7

This script implements advanced statistical analysis techniques to identify
subtle patterns and correlations in vulnerability test results, helping to
discover new vulnerability categories and predict potential exploits.
"""

import argparse
import json
import os
import sys
from typing import Dict, List, Any, Optional, Set, Tuple
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter, defaultdict
from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.manifold import TSNE
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import networkx as nx

# Ensure NLTK resources are available
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class VulnerabilityPatternAnalyzer:
    """
    Advanced statistical analysis of vulnerability patterns across test results.
    """
    
    def __init__(self):
        """Initialize the pattern analyzer."""
        self.test_results = []
        self.prompts = []
        self.responses = []
        self.vulnerability_data = pd.DataFrame()
        self.clusters = {}
        self.correlation_matrix = None
        self.similarity_matrix = None
        self.stop_words = set(stopwords.words('english'))
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=1000, 
            stop_words='english',
            ngram_range=(1, 3)
        )
        
    def load_test_results(self, file_paths: List[str]):
        """
        Load test results from multiple files.
        
        Args:
            file_paths: List of file paths to load test results from
        """
        all_results = []
        all_prompts = []
        all_responses = []
        
        for file_path in file_paths:
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                
                # Handle different result formats
                if "test_results" in data:
                    results = data["test_results"]
                elif isinstance(data, list):
                    results = data
                else:
                    results = [data]
                    
                # Extract prompts and responses
                for result in results:
                    if "test_case" in result and "response" in result:
                        all_prompts.append(result["test_case"])
                        all_responses.append(result["response"])
                    elif "prompt" in result and "response" in result:
                        all_prompts.append(result["prompt"])
                        all_responses.append(result["response"])
                    
                all_results.extend(results)
                    
                print(f"Loaded {len(results)} results from {file_path}")
                
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
        
        self.test_results = all_results
        self.prompts = all_prompts
        self.responses = all_responses
        
        print(f"Total results loaded: {len(self.test_results)}")
        
        # Convert to DataFrame for easier analysis
        self._convert_to_dataframe()
        
    def _convert_to_dataframe(self):
        """Convert test results to a pandas DataFrame for analysis."""
        data = []
        
        for result in self.test_results:
            # Extract common fields with fallbacks
            row = {
                "id": result.get("id", result.get("test_id", result.get("vulnerability_id", "unknown"))),
                "category": result.get("category", "unknown"),
                "severity": result.get("severity", "unknown"),
                "success": result.get("vulnerability_detected", result.get("success", False)),
                "prompt": result.get("test_case", result.get("prompt", "")),
                "response": result.get("response", ""),
                "model": result.get("model", "unknown"),
                "mode": result.get("mode", "unknown"),
                "timestamp": result.get("timestamp", "")
            }
            
            # Handle categories as lists
            if isinstance(row["category"], list):
                row["primary_category"] = row["category"][0] if row["category"] else "unknown"
                row["all_categories"] = ", ".join(row["category"])
            else:
                row["primary_category"] = row["category"]
                row["all_categories"] = row["category"]
                
            data.append(row)
            
        self.vulnerability_data = pd.DataFrame(data)
        
    def compute_basic_statistics(self):
        """
        Compute basic statistics on the vulnerability data.
        
        Returns:
            dict: Dictionary containing basic statistics
        """
        if self.vulnerability_data.empty:
            print("No data available for analysis")
            return {}
        
        stats = {
            "total_tests": len(self.vulnerability_data),
            "successful_tests": self.vulnerability_data["success"].sum(),
            "success_rate": self.vulnerability_data["success"].mean() * 100,
            "category_counts": self.vulnerability_data["primary_category"].value_counts().to_dict(),
            "model_counts": self.vulnerability_data["model"].value_counts().to_dict(),
            "mode_counts": self.vulnerability_data["mode"].value_counts().to_dict(),
            "severity_counts": self.vulnerability_data["severity"].value_counts().to_dict()
        }
        
        # Success rates by category
        category_success = self.vulnerability_data.groupby("primary_category")["success"].agg(["mean", "count"])
        stats["category_success_rates"] = {
            cat: {"success_rate": rate * 100, "count": count}
            for cat, (rate, count) in category_success.iterrows()
        }
        
        # Success rates by model
        if "unknown" not in self.vulnerability_data["model"].unique():
            model_success = self.vulnerability_data.groupby("model")["success"].agg(["mean", "count"])
            stats["model_success_rates"] = {
                model: {"success_rate": rate * 100, "count": count}
                for model, (rate, count) in model_success.iterrows()
            }
            
        # Success rates by mode
        if "unknown" not in self.vulnerability_data["mode"].unique():
            mode_success = self.vulnerability_data.groupby("mode")["success"].agg(["mean", "count"])
            stats["mode_success_rates"] = {
                mode: {"success_rate": rate * 100, "count": count}
                for mode, (rate, count) in mode_success.iterrows()
            }
        
        return stats
    
    def perform_textual_analysis(self):
        """
        Perform textual analysis on prompts and responses to identify patterns.
        
        Returns:
            dict: Dictionary containing textual analysis results
        """
        if not self.prompts or not self.responses:
            print("No text data available for analysis")
            return {}
        
        # Combined successful responses
        successful_indices = self.vulnerability_data[self.vulnerability_data["success"] == True].index
        successful_responses = [self.responses[i] for i in successful_indices if i < len(self.responses)]
        
        if not successful_responses:
            print("No successful responses available for analysis")
            return {}
        
        # Perform TF-IDF analysis on successful responses
        try:
            tfidf_matrix = self.tfidf_vectorizer.fit_transform(successful_responses)
            feature_names = self.tfidf_vectorizer.get_feature_names_out()
            
            # Get top terms overall
            tfidf_sums = tfidf_matrix.sum(axis=0)
            tfidf_scores = [(feature_names[i], tfidf_sums[0, i]) for i in range(len(feature_names))]
            top_terms = sorted(tfidf_scores, key=lambda x: x[1], reverse=True)[:30]
            
            # Get category-specific terms
            category_terms = {}
            for category in self.vulnerability_data["primary_category"].unique():
                if category == "unknown":
                    continue
                    
                cat_indices = self.vulnerability_data[
                    (self.vulnerability_data["primary_category"] == category) & 
                    (self.vulnerability_data["success"] == True)
                ].index
                
                cat_responses = [self.responses[i] for i in cat_indices if i < len(self.responses)]
                
                if not cat_responses:
                    continue
                    
                cat_matrix = self.tfidf_vectorizer.transform(cat_responses)
                cat_sums = cat_matrix.sum(axis=0)
                cat_scores = [(feature_names[i], cat_sums[0, i]) for i in range(len(feature_names))]
                category_terms[category] = sorted(cat_scores, key=lambda x: x[1], reverse=True)[:15]
            
            # Term co-occurrence in successful responses
            co_occurrence = defaultdict(int)
            for response in successful_responses:
                tokens = word_tokenize(response.lower())
                tokens = [token for token in tokens if token.isalpha() and token not in self.stop_words]
                
                for i in range(len(tokens)):
                    for j in range(i + 1, min(i + 6, len(tokens))):
                        if tokens[i] != tokens[j]:
                            term_pair = tuple(sorted([tokens[i], tokens[j]]))
                            co_occurrence[term_pair] += 1
            
            top_co_occurrences = sorted(co_occurrence.items(), key=lambda x: x[1], reverse=True)[:50]
            
            return {
                "top_terms": top_terms,
                "category_specific_terms": category_terms,
                "term_co_occurrences": top_co_occurrences
            }
            
        except Exception as e:
            print(f"Error in textual analysis: {e}")
            return {}
    
    def cluster_vulnerabilities(self, n_clusters=5):
        """
        Cluster vulnerabilities based on responses to identify related patterns.
        
        Args:
            n_clusters: Number of clusters to identify
            
        Returns:
            dict: Clustering results
        """
        if not self.responses:
            print("No responses available for clustering")
            return {}
            
        # Vectorize responses
        try:
            tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.responses)
            
            # Reduce dimensions for visualization
            pca = PCA(n_components=min(50, tfidf_matrix.shape[1], tfidf_matrix.shape[0] - 1))
            reduced_features = pca.fit_transform(tfidf_matrix.toarray())
            
            # Further reduce for visualization
            tsne = TSNE(n_components=2, random_state=42)
            embedded_features = tsne.fit_transform(reduced_features)
            
            # Perform clustering
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            clusters = kmeans.fit_predict(reduced_features)
            
            # Store clustering information
            self.clusters = {
                "cluster_assignments": clusters,
                "embedded_features": embedded_features,
                "reduced_features": reduced_features,
                "n_clusters": n_clusters
            }
            
            # Get cluster statistics
            cluster_stats = {}
            for i in range(n_clusters):
                cluster_indices = np.where(clusters == i)[0]
                cluster_success_rate = sum(self.vulnerability_data.iloc[idx]["success"] for idx in cluster_indices if idx < len(self.vulnerability_data)) / len(cluster_indices)
                
                # Get most frequent categories in this cluster
                cluster_categories = [self.vulnerability_data.iloc[idx]["primary_category"] for idx in cluster_indices if idx < len(self.vulnerability_data)]
                category_counts = Counter(cluster_categories)
                top_categories = category_counts.most_common(3)
                
                # Get characteristic terms for this cluster
                cluster_responses = [self.responses[idx] for idx in cluster_indices if idx < len(self.responses)]
                if cluster_responses:
                    try:
                        cluster_matrix = self.tfidf_vectorizer.transform(cluster_responses)
                        cluster_avg = cluster_matrix.mean(axis=0)
                        feature_names = self.tfidf_vectorizer.get_feature_names_out()
                        
                        important_terms = [(feature_names[j], cluster_avg[0, j]) for j in range(len(feature_names))]
                        top_terms = sorted(important_terms, key=lambda x: x[1], reverse=True)[:10]
                    except:
                        top_terms = []
                else:
                    top_terms = []
                
                cluster_stats[i] = {
                    "size": len(cluster_indices),
                    "success_rate": cluster_success_rate * 100,
                    "top_categories": top_categories,
                    "characteristic_terms": top_terms
                }
            
            return {
                "n_clusters": n_clusters,
                "cluster_stats": cluster_stats,
                "visualization_data": embedded_features.tolist(),
                "cluster_labels": clusters.tolist()
            }
            
        except Exception as e:
            print(f"Error in clustering: {e}")
            return {}
            
    def compute_correlation_matrix(self):
        """
        Compute correlation matrix between different vulnerability categories.
        
        Returns:
            DataFrame: Correlation matrix
        """
        if self.vulnerability_data.empty:
            return None
            
        # Create category presence matrix
        all_categories = set()
        for cat_list in self.vulnerability_data["all_categories"]:
            categories = [c.strip() for c in cat_list.split(",")]
            all_categories.update(categories)
        
        category_matrix = pd.DataFrame(0, index=self.vulnerability_data.index, 
                                      columns=list(all_categories))
        
        for idx, cat_list in enumerate(self.vulnerability_data["all_categories"]):
            categories = [c.strip() for c in cat_list.split(",")]
            for cat in categories:
                if cat in category_matrix.columns:
                    category_matrix.loc[idx, cat] = 1
        
        # Compute correlation matrix
        self.correlation_matrix = category_matrix.corr()
        return self.correlation_matrix
    
    def compute_similarity_matrix(self):
        """
        Compute similarity matrix between test cases based on responses.
        
        Returns:
            numpy.ndarray: Similarity matrix
        """
        if not self.responses:
            return None
            
        try:
            # Compute TF-IDF matrix
            tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.responses)
            
            # Compute cosine similarity
            self.similarity_matrix = cosine_similarity(tfidf_matrix)
            return self.similarity_matrix
            
        except Exception as e:
            print(f"Error in similarity computation: {e}")
            return None
    
    def identify_patterns(self):
        """
        Identify potential new vulnerability patterns from the data.
        
        Returns:
            dict: Identified patterns
        """
        patterns = {}
        
        # Get successful tests
        successful = self.vulnerability_data[self.vulnerability_data["success"] == True]
        
        if successful.empty:
            return patterns
            
        # Pattern 1: Common terms in successful tests by category
        try:
            textual_analysis = self.perform_textual_analysis()
            if textual_analysis and "category_specific_terms" in textual_analysis:
                patterns["category_patterns"] = {}
                
                for category, terms in textual_analysis["category_specific_terms"].items():
                    # Only consider top 5 terms with good scores
                    significant_terms = [term for term, score in terms[:5] if score > 0.1]
                    if significant_terms:
                        patterns["category_patterns"][category] = significant_terms
        except:
            pass
            
        # Pattern 2: Highly correlated categories
        try:
            if self.correlation_matrix is None:
                self.compute_correlation_matrix()
                
            if self.correlation_matrix is not None:
                # Find pairs with correlation > 0.5
                corr_pairs = []
                for i in range(len(self.correlation_matrix.columns)):
                    for j in range(i+1, len(self.correlation_matrix.columns)):
                        col1, col2 = self.correlation_matrix.columns[i], self.correlation_matrix.columns[j]
                        corr = self.correlation_matrix.loc[col1, col2]
                        if corr > 0.5:  # Strong positive correlation
                            corr_pairs.append((col1, col2, corr))
                
                if corr_pairs:
                    patterns["correlated_categories"] = sorted(corr_pairs, key=lambda x: x[2], reverse=True)
        except:
            pass
            
        # Pattern 3: Cluster-based patterns
        try:
            if not self.clusters:
                self.cluster_vulnerabilities()
                
            if self.clusters and "cluster_stats" in self.clusters:
                # Find promising clusters with high success rates
                promising_clusters = {}
                for cluster_id, stats in self.clusters["cluster_stats"].items():
                    if stats["success_rate"] > 75 and stats["size"] >= 5:
                        promising_clusters[cluster_id] = {
                            "categories": [cat for cat, count in stats["top_categories"]],
                            "terms": [term for term, score in stats["characteristic_terms"][:5]],
                            "success_rate": stats["success_rate"]
                        }
                
                if promising_clusters:
                    patterns["cluster_patterns"] = promising_clusters
        except:
            pass
            
        # Pattern 4: Similar successful tests
        try:
            if self.similarity_matrix is None:
                self.compute_similarity_matrix()
                
            if self.similarity_matrix is not None and len(successful) > 1:
                successful_indices = successful.index.tolist()
                if len(successful_indices) > 1:
                    # Extract similarity submatrix for successful tests
                    sim_submatrix = self.similarity_matrix[np.ix_(successful_indices, successful_indices)]
                    
                    # Set diagonal to 0 to ignore self-similarity
                    np.fill_diagonal(sim_submatrix, 0)
                    
                    # Find highly similar pairs
                    similar_pairs = []
                    for i in range(sim_submatrix.shape[0]):
                        for j in range(i+1, sim_submatrix.shape[0]):
                            if sim_submatrix[i, j] > 0.7:  # High similarity threshold
                                idx1, idx2 = successful_indices[i], successful_indices[j]
                                cat1 = self.vulnerability_data.iloc[idx1]["primary_category"]
                                cat2 = self.vulnerability_data.iloc[idx2]["primary_category"]
                                similar_pairs.append((idx1, idx2, cat1, cat2, sim_submatrix[i, j]))
                    
                    if similar_pairs:
                        patterns["similar_tests"] = sorted(similar_pairs, key=lambda x: x[4], reverse=True)
        except:
            pass
        
        return patterns
    
    def suggest_new_test_cases(self, num_suggestions=5):
        """
        Suggest new test cases based on identified patterns.
        
        Args:
            num_suggestions: Number of test cases to suggest
            
        Returns:
            list: Suggested test cases
        """
        suggestions = []
        
        # First identify patterns
        patterns = self.identify_patterns()
        
        # Generate suggestions based on patterns
        if "category_patterns" in patterns:
            for category, terms in patterns["category_patterns"].items():
                if len(terms) >= 3:  # Need enough terms for a good suggestion
                    # Build a suggestion based on category and characteristic terms
                    suggestion = {
                        "category": category,
                        "title": f"New {category} Test",
                        "test_case": f"Test for {category} using terms: {', '.join(terms)}",
                        "rationale": f"Based on characteristic terms found in successful {category} vulnerabilities: {', '.join(terms)}"
                    }
                    suggestions.append(suggestion)
        
        # Generate suggestions based on correlated categories
        if "correlated_categories" in patterns and patterns["correlated_categories"]:
            for cat1, cat2, corr in patterns["correlated_categories"][:3]:
                suggestion = {
                    "category": [cat1, cat2],
                    "title": f"{cat1}-{cat2} Hybrid Test",
                    "test_case": f"Test combining elements of {cat1} and {cat2} vulnerabilities",
                    "rationale": f"Based on strong correlation ({corr:.2f}) between {cat1} and {cat2} vulnerabilities"
                }
                suggestions.append(suggestion)
        
        # Generate suggestions based on promising clusters
        if "cluster_patterns" in patterns:
            for cluster_id, data in patterns["cluster_patterns"].items():
                if len(data["terms"]) >= 3:
                    categories = " and ".join(data["categories"][:2])
                    suggestion = {
                        "category": data["categories"],
                        "title": f"Cluster {cluster_id} Test",
                        "test_case": f"Test based on cluster {cluster_id} involving {categories} with terms: {', '.join(data['terms'])}",
                        "rationale": f"Based on cluster with {data['success_rate']:.1f}% success rate using terms: {', '.join(data['terms'])}"
                    }
                    suggestions.append(suggestion)
        
        # Return top suggestions
        return suggestions[:num_suggestions]
    
    def generate_visualization(self, output_dir="./visualizations"):
        """Generate visualizations of the vulnerability patterns."""
        if self.vulnerability_data.empty:
            print("No data available for visualization")
            return
            
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # 1. Success rates by category
        try:
            plt.figure(figsize=(12, 8))
            cat_success = self.vulnerability_data.groupby("primary_category")["success"].mean().sort_values(ascending=False)
            cat_counts = self.vulnerability_data.groupby("primary_category").size()
            
            # Filter to categories with at least 3 samples
            cat_success = cat_success[cat_counts >= 3]
            
            ax = cat_success.plot(kind='bar', color='skyblue')
            plt.title('Vulnerability Success Rates by Category', fontsize=14)
            plt.xlabel('Category', fontsize=12)
            plt.ylabel('Success Rate', fontsize=12)
            plt.xticks(rotation=45, ha='right')
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            plt.tight_layout()
            
            # Add count labels
            for i, v in enumerate(cat_success):
                cat = cat_success.index[i]
                count = cat_counts[cat]
                ax.text(i, v + 0.02, f"n={count}", ha='center', fontsize=9)
            
            plt.savefig(os.path.join(output_dir, "category_success_rates.png"), dpi=300)
            plt.close()
        except Exception as e:
            print(f"Error generating category success rates visualization: {e}")
        
        # 2. Correlation matrix heatmap
        try:
            if self.correlation_matrix is None:
                self.compute_correlation_matrix()
                
            if self.correlation_matrix is not None:
                plt.figure(figsize=(12, 10))
                sns.heatmap(self.correlation_matrix, annot=True, cmap='coolwarm', center=0, fmt=".2f", 
                           linewidths=.5, cbar_kws={"shrink": .8})
                plt.title('Correlation Between Vulnerability Categories', fontsize=14)
                plt.xticks(rotation=45, ha='right')
                plt.yticks(rotation=0)
                plt.tight_layout()
                plt.savefig(os.path.join(output_dir, "category_correlation.png"), dpi=300)
                plt.close()
        except Exception as e:
            print(f"Error generating correlation heatmap: {e}")
        
        # 3. Cluster visualization
        try:
            if self.clusters and "visualization_data" in self.clusters:
                plt.figure(figsize=(10, 8))
                embedded = np.array(self.clusters["visualization_data"])
                clusters = np.array(self.clusters["cluster_labels"])
                
                for i in range(self.clusters["n_clusters"]):
                    cluster_points = embedded[clusters == i]
                    plt.scatter(cluster_points[:, 0], cluster_points[:, 1], label=f'Cluster {i}', alpha=0.7)
                
                plt.title('Vulnerability Clusters Visualization', fontsize=14)
                plt.xlabel('t-SNE Dimension 1', fontsize=12)
                plt.ylabel('t-SNE Dimension 2', fontsize=12)
                plt.legend()
                plt.grid(alpha=0.3)
                plt.tight_layout()
                plt.savefig(os.path.join(output_dir, "vulnerability_clusters.png"), dpi=300)
                plt.close()
        except Exception as e:
            print(f"Error generating cluster visualization: {e}")
        
        # 4. Success rate by model and mode
        try:
            if "unknown" not in self.vulnerability_data["model"].unique():
                plt.figure(figsize=(10, 6))
                model_mode_success = self.vulnerability_data.groupby(["model", "mode"])["success"].mean().unstack()
                model_mode_success.plot(kind='bar')
                plt.title('Success Rates by Model and Mode', fontsize=14)
                plt.xlabel('Model', fontsize=12)
                plt.ylabel('Success Rate', fontsize=12)
                plt.xticks(rotation=45, ha='right')
                plt.grid(axis='y', linestyle='--', alpha=0.7)
                plt.legend(title='Mode')
                plt.tight_layout()
                plt.savefig(os.path.join(output_dir, "model_mode_success.png"), dpi=300)
                plt.close()
        except Exception as e:
            print(f"Error generating model/mode success rates visualization: {e}")
        
        # 5. Network graph of term co-occurrences
        try:
            textual_analysis = self.perform_textual_analysis()
            if textual_analysis and "term_co_occurrences" in textual_analysis:
                co_occurrences = textual_analysis["term_co_occurrences"][:30]  # Top 30 co-occurrences
                
                G = nx.Graph()
                for (term1, term2), weight in co_occurrences:
                    G.add_edge(term1, term2, weight=weight)
                
                plt.figure(figsize=(12, 12))
                pos = nx.spring_layout(G, k=0.3, iterations=50)
                
                # Node sizes based on degree
                node_size = [G.degree(node) * 100 for node in G.nodes()]
                
                # Edge widths based on weight
                edge_width = [G[u][v]['weight'] * 0.5 for u, v in G.edges()]
                
                nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color='skyblue', alpha=0.8)
                nx.draw_networkx_edges(G, pos, width=edge_width, alpha=0.5, edge_color='gray')
                nx.draw_networkx_labels(G, pos, font_size=10)
                
                plt.title('Term Co-occurrence Network in Successful Vulnerabilities', fontsize=14)
                plt.axis('off')
                plt.tight_layout()
                plt.savefig(os.path.join(output_dir, "term_co_occurrence_network.png"), dpi=300)
                plt.close()
        except Exception as e:
            print(f"Error generating term co-occurrence network: {e}")
    
    def export_analysis_report(self, output_path, include_suggestions=True):
        """
        Generate a comprehensive analysis report.
        
        Args:
            output_path: Path to save the report
            include_suggestions: Whether to include test case suggestions
        
        Returns:
            bool: Success status
        """
        if self.vulnerability_data.empty:
            print("No data available for analysis")
            return False
            
        try:
            # Collect all analysis results
            stats = self.compute_basic_statistics()
            textual_analysis = self.perform_textual_analysis()
            
            if not self.clusters:
                self.cluster_vulnerabilities()
                
            if self.correlation_matrix is None:
                self.compute_correlation_matrix()
                
            patterns = self.identify_patterns()
            
            # Generate test case suggestions if requested
            suggestions = []
            if include_suggestions:
                suggestions = self.suggest_new_test_cases(num_suggestions=10)
            
            # Build the report
            report = {
                "title": "Claude 3.7 Vulnerability Analysis Report",
                "generated_at": datetime.datetime.now().isoformat(),
                "data_summary": {
                    "total_tests": len(self.vulnerability_data),
                    "total_successful": self.vulnerability_data["success"].sum(),
                    "overall_success_rate": stats.get("success_rate", 0)
                },
                "statistics": stats,
                "textual_analysis": textual_analysis,
                "identified_patterns": patterns,
                "suggested_test_cases": suggestions
            }
            
            # Write the report
            with open(output_path, 'w') as f:
                json.dump(report, f, indent=2)
                
            print(f"Analysis report saved to {output_path}")
            return True
            
        except Exception as e:
            print(f"Error generating analysis report: {e}")
            return False
    
    def export_test_case_suggestions(self, output_path, format_type="json"):
        """
        Export suggested test cases in various formats.
        
        Args:
            output_path: Path to save the suggestions
            format_type: Format type ('json' or 'test_suite')
            
        Returns:
            bool: Success status
        """
        suggestions = self.suggest_new_test_cases(num_suggestions=15)
        
        if not suggestions:
            print("No test case suggestions available")
            return False
            
        try:
            if format_type == "json":
                with open(output_path, 'w') as f:
                    json.dump(suggestions, f, indent=2)
            
            elif format_type == "test_suite":
                # Convert to test suite format
                test_suite = {
                    "name": "Auto-Generated Vulnerability Test Suite",
                    "description": "Test cases generated based on statistical pattern analysis",
                    "version": "1.0",
                    "created": datetime.datetime.now().isoformat(),
                    "test_cases": []
                }
                
                for i, suggestion in enumerate(suggestions):
                    test_case = {
                        "vulnerability_id": f"CLAUDE37-PATTERN-{i+1:03d}",
                        "title": suggestion["title"],
                        "category": suggestion["category"] if isinstance(suggestion["category"], list) else [suggestion["category"]],
                        "severity": "Medium",  # Default severity
                        "test_case": suggestion["test_case"],
                        "rationale": suggestion["rationale"],
                        "source": "auto-generated"
                    }
                    
                    test_suite["test_cases"].append(test_case)
                
                with open(output_path, 'w') as f:
                    json.dump(test_suite, f, indent=2)
            
            print(f"Test case suggestions exported to {output_path}")
            return True
            
        except Exception as e:
            print(f"Error exporting test case suggestions: {e}")
            return False


def main():
    """Main function to run the vulnerability pattern analyzer."""
    parser = argparse.ArgumentParser(description="Advanced Pattern Analysis for Claude 3.7 Vulnerabilities")
    parser.add_argument("--results", nargs="+", required=True, help="Paths to result files to analyze")
    parser.add_argument("--report", help="Path to save the analysis report")
    parser.add_argument("--visualize", action="store_true", help="Generate visualizations")
    parser.add_argument("--vis-dir", default="./visualizations", help="Directory to save visualizations")
    parser.add_argument("--suggest-tests", help="Path to save suggested test cases")
    parser.add_argument("--format", choices=["json", "test_suite"], default="test_suite", help="Format for suggested tests")
    
    args = parser.parse_args()
    
    # Create the analyzer
    analyzer = VulnerabilityPatternAnalyzer()
    
    # Load test results
    analyzer.load_test_results(args.results)
    
    # Generate visualizations if requested
    if args.visualize:
        analyzer.generate_visualization(args.vis_dir)
    
    # Generate analysis report if requested
    if args.report:
        analyzer.export_analysis_report(args.report)
    
    # Export test case suggestions if requested
    if args.suggest_tests:
        analyzer.export_test_case_suggestions(args.suggest_tests, args.format)
    
    # If no output options specified, print basic statistics
    if not any([args.visualize, args.report, args.suggest_tests]):
        stats = analyzer.compute_basic_statistics()
        print("\nBasic Statistics:")
        print(f"Total tests: {stats.get('total_tests', 0)}")
        print(f"Successful tests: {stats.get('successful_tests', 0)}")
        print(f"Overall success rate: {stats.get('success_rate', 0):.2f}%")
        
        print("\nSuccess rates by category:")
        for cat, data in stats.get("category_success_rates", {}).items():
            print(f"  {cat}: {data['success_rate']:.2f}% ({data['count']} tests)")

if __name__ == "__main__":
    main()
