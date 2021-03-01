#include <vector>
#include <iostream>
#include <utility>

// For Maze

using namespace std;

using Graph = vector<vector< int>>;
using bGraph = vector<vector< bool>>;

void print_graph(const Graph& g);
void print_path(const Graph& g, const Graph& path, int ex, int ey);
void copyGraph(const Graph& g, Graph& n);

#define FMT "%3d "

void init_graph(Graph &graph, int rows, int cols, int val)
{
    graph.resize(rows);
    for (int i = 0; i < rows; ++i) {
        graph[i].resize(cols, val);
    }
}

void init_bGraph(bGraph &graph, int rows, int cols)
{
    graph.resize(rows);
    for (int i = 0; i < rows; ++i) {
        graph[i].resize(cols, 0);
    }
}


int getShortestPath(vector<int>& set_queue, const Graph& dist)
{
    int index;
    int min_dist = 999999999;
    int ret = -1;
    for (size_t i = 0; i < set_queue.size(); ++i) {
        int val = set_queue[i];
        int x = val >> 16, y = val & 0xffff;
        if (dist[y][x] < min_dist) {
            index = i;
            min_dist = dist[y][x];
            ret = val;
        }
    }
   
    set_queue.erase(set_queue.begin() + index);
    return ret;
}

constexpr int BLK = -1;

void dijkstra(const Graph &graph, int sx, int sy, int ex, int ey, Graph &path, Graph &dist)
{
    int h = graph.size(), w = graph[0].size();

    bGraph visited;
    //Graph path;
    ///Graph dist;

    vector<int > set_queue;

    init_bGraph(visited, h, w);
    init_graph(path, h, w, -999999);
    init_graph(dist, h, w, -999999);

    set_queue.push_back((sx << 16) + sy);

    dist[sy][sx] = 0;
    path[sy][sx] = -1;
    visited[sy][sx] = 1;
    static const vector<pair<int,int> > steps = {{0,1},{1,0},{0,-1},{-1,0}};

    while (set_queue.size()) {
        int val = getShortestPath(set_queue, dist);
        int ssx = val >> 16;
        int ssy = val & 0xffff;

        for (const auto& step : steps) {
            int sxt = ssx + step.second;
            int syt = ssy + step.first;
            if (sxt < 0 || sxt >= w || syt < 0 || syt >= h)
                continue;
            if (graph[syt][sxt] == BLK)
                continue;
            int stepdist = (graph[syt][sxt] == 0) ? 1 : graph[syt][sxt];

            if (visited[syt][sxt])
#if 0
                continue;
#else
            {
                //for edge value presence
                if (dist[syt][sxt] <= (dist[ssy][ssx] + stepdist))
                    continue;
            }
#endif 
            visited[syt][sxt] = 1;
            dist[syt][sxt] = dist[ssy][ssx] + stepdist;
            path[syt][sxt] = (ssx << 16) + ssy;
            set_queue.push_back((sxt << 16) + syt);
        }
    }

    return;

}

void print_graph(const Graph& g)
{
    printf("\n");
    int h = g.size(), w = g[0].size();
    for (int i = -1; i < w; i++) {
        printf(FMT, i);
    } printf("\n");

    for (int i = 0; i < h; i++) {
        for (int j = -1; j < w; j++) {
            if (j == -1) printf(FMT, i);
            else printf(FMT, g[i][j]);
        } printf("\n");
    }
}

void copyGraph(const Graph& g, Graph& n)
{
    int h = g.size(), w = g[0].size();
    n.reserve(h * w);
    n.resize(h);
    for (int i = 0; i < h; ++i) {
        n[i].resize(w);
        for (int j = 0; j < w; ++j) {
            n[i][j] = g[i][j];
        }
    }
}

void print_path(const Graph& g, const Graph& path, int ex, int ey)
{
    Graph s;
    copyGraph(g, s);
    int x = ex, y = ey;
    s[y][x] = 7;
    int prev = 1;
    do {
        prev = path[y][x];
        x = prev >> 16;
        y = prev & 0xffff;
        if (prev == -1) 
            break;
        s[y][x] = 7;
    } while (prev != -1);

    print_graph(s);
}

void case2(int argc, char **argv)
{

    Graph graph = {
        {0, 0, 0, -1, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, -1, 0, 5, 2, 0, 0, 0},
        {0, 0, 0, -1, 0, -1, 0, 0, 0, 0},
        {0, 0, 0,  0, 0, -1, 0, 0, 0, -1},
        {9, 1, 3, -1, 0, -1, 0, 0, -1, 0},
        {3, 1, 9, -1, 0, -1, -1, -1, 0, 0},
        {2, 9, 9, -1, 0, -1, 0, 0, 0, 0},
        {0, 5, 5, -1, 0, -1, 0, 0, 0, 0},
        {0, 0, 0, -1, 0, 5, 2, 2, 0, 0},
        {0, 0, 0, -1, 0, 0, 0, 0, 0, 0}
    };

    Graph path, dist;

    int h = 10, w = 10;
    int sx = 0, sy = 0, ex = 9, ey = 1; 
    if (argc == 5) {
        sx = atoi(argv[1]);
        sy = atoi(argv[2]);
        ex = atoi(argv[3]);
        ey = atoi(argv[4]);
    }
    //init_graph(graph, h, w, 0);
    printf("args: h:%d,w:%d (%d,%d)->(%d,%d)\n", h, w, sx, sy, ex, ey);
    print_graph(graph);
    //cout << "tranverse bfs :\n";
    //tranversebfs(graph, sx, sy, ex, ey);
    //cout << "tranverse dfs :\n";
    //tranversedfs(graph, sx, sy, ex, ey);
    dijkstra(graph, sx, sy, ex, ey, path, dist);
    //print_graph(path);
    //print_graph(dist);
    print_path(graph, path, ex, ey);

}

void case1(int argc, char **argv)
{
    Graph graph;
    Graph path, dist;

    int h = 9, w = 9;
    int sx = 0, sy = 0, ex = 3, ey = 2; 
    if (argc == 7) {
        h = atoi(argv[1]);
        w = atoi(argv[2]);
        sx = atoi(argv[3]);
        sy = atoi(argv[4]);
        ex = atoi(argv[5]);
        ey = atoi(argv[6]);
    }
    init_graph(graph, h, w, 0);
    printf("args: h:%d,w:%d (%d,%d)->(%d,%d)\n", h, w, sx, sy, ex, ey);
    print_graph(graph);
    //cout << "tranverse bfs :\n";
    //tranversebfs(graph, sx, sy, ex, ey);
    //cout << "tranverse dfs :\n";
    //tranversedfs(graph, sx, sy, ex, ey);
    dijkstra(graph, sx, sy, ex, ey, path, dist);
    print_path(graph, path, ex, ey);
}

int main(int argc, char **argv)
{
    //case1(argc, argv); without blk
    case2(argc, argv); // with blk

    return 0;
}

