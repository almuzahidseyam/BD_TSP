#pragma GCC optimize("O3,unroll-loops")
#pragma GCC target("avx2,bmi,bmi2,lzcnt,popcnt")

#include <iostream>
#include <vector>
#include <cmath>
#include <iomanip>

using namespace std;

const double INF = 1e9;

int main() {
    // Fast I/O for Competitive Programming
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    if (!(cin >> n)) return 0;

    // Use 1D vector for better cache locality instead of vector<vector>
    vector<double> dist(n * n);
    for (int i = 0; i < n * n; ++i) {
        cin >> dist[i];
    }

    int num_masks = 1 << n;
    vector<double> dp(num_masks * n, INF);
    vector<int> parent(num_masks * n, -1);

    // Base case: Start at node 0
    dp[1 * n + 0] = 0.0;

    for (int mask = 1; mask < num_masks; ++mask) {
        int temp_mask = mask;
        // Optimization: Use __builtin_ctz to iterate ONLY over set bits
        while (temp_mask > 0) {
            int u = __builtin_ctz(temp_mask);
            temp_mask ^= (1 << u);
            
            double current_cost = dp[mask * n + u];
            if (current_cost >= INF) continue;

            // Iterate over UNVISITED bits using inverted mask
            int unvisited = ((num_masks - 1) ^ mask);
            while (unvisited > 0) {
                int v = __builtin_ctz(unvisited);
                unvisited ^= (1 << v);

                int next_mask = mask | (1 << v);
                double new_cost = current_cost + dist[u * n + v];
                
                if (new_cost < dp[next_mask * n + v]) {
                    dp[next_mask * n + v] = new_cost;
                    parent[next_mask * n + v] = u;
                }
            }
        }
    }

    // Find the minimum cost to return to node 0
    double min_cost = INF;
    int last_node = -1;
    int full_mask = num_masks - 1;

    for (int i = 1; i < n; ++i) {
        double cost = dp[full_mask * n + i] + dist[i * n + 0];
        if (cost < min_cost) {
            min_cost = cost;
            last_node = i;
        }
    }

    // Reconstruct path
    vector<int> path;
    int curr_mask = full_mask;
    int curr_node = last_node;

    while (curr_node != -1) {
        path.push_back(curr_node);
        int p = parent[curr_mask * n + curr_node];
        curr_mask ^= (1 << curr_node);
        curr_node = p;
    }

    cout << fixed << setprecision(2) << min_cost << "\n";
    for (int i = path.size() - 1; i >= 0; --i) {
        cout << path[i] << " ";
    }
    cout << 0 << "\n"; 

    return 0;
}
