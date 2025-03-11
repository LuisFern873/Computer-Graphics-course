#define _USE_MATH_DEFINES 
#include <iostream>
#include <vector>
#include <algorithm>
#include <stack>
#include <cmath>
#include <chrono>
#include <functional>

using namespace std;
using namespace chrono;

struct Point {
    double x, y;
};

Point p0;

Point nextToTop(stack<Point>& S) {
    Point p = S.top();
    S.pop();
    Point res = S.top();
    S.push(p);
    return res;
}

void swap(Point &p1, Point &p2) {
    Point temp = p1;
    p1 = p2;
    p2 = temp;
}

double distSq(Point p1, Point p2) {
    return (p1.x - p2.x) * (p1.x - p2.x) + (p1.y - p2.y) * (p1.y - p2.y);
}

double orientation(Point p, Point q, Point r) {
    double val = (q.y - p.y) * (r.x - q.x) -
              (q.x - p.x) * (r.y - q.y);
    if (val == 0) return 0;  // collinear
    return (val > 0) ? 1 : 2; // clock or counterclock wise
}

bool compare(const Point& p1, const Point& p2) {
    int o = orientation(p0, p1, p2);
    if (o == 0)
        return distSq(p0, p2) >= distSq(p0, p1);
    return (o == 2);
}

vector<Point> jarvisMarch(vector<Point>& points) {
    int n = points.size();
    vector<Point> hull;
    
    int l = 0;
    for (int i = 1; i < n; i++)
        if (points[i].x < points[l].x)
            l = i;

    int p = l, q;
    do {
        hull.push_back(points[p]);

        q = (p + 1) % n;
        for (int i = 0; i < n; i++) {
            if (orientation(points[p], points[i], points[q]) == 2)
                q = i;
        }
        p = q;

    } while (p != l);

    return hull;
}

// for (auto point : hull)
//     cout << "(" << point.x << ", " << point.y << ")\n";

stack<Point> grahamScan(vector<Point>& points) {
    int n = points.size();

    double ymin = points[0].y, min = 0;
    for (int i = 1; i < n; i++) {
        double y = points[i].y;
        if ((y < ymin) || (ymin == y && points[i].x < points[min].x))
            ymin = points[i].y, min = i;
    }
    swap(points[0], points[min]);

    p0 = points[0];
    sort(points.begin() + 1, points.end(), compare);

    stack<Point> S;
    S.push(points[0]);
    S.push(points[1]);
    S.push(points[2]);

    for (int i = 3; i < n; i++) {
        while (S.size() > 1 && orientation(nextToTop(S), S.top(), points[i]) != 2)
            S.pop();
        S.push(points[i]);
    }
    return S;
}

// while (!S.empty()) {
//     Point p = S.top();
//     cout << "(" << p.x << ", " << p.y << ")" << endl;
//     S.pop();
// }


double randomDouble(double min, double max) {
    return min + (max - min) * (static_cast<double>(rand()) / RAND_MAX);
}

vector<Point> generateRandomPointsInCircle(int n) {
    vector<Point> points;
    double R = 1'000.0;
    for (int i = 0; i < n; ++i) {
        double angle = randomDouble(0, 2 * M_PI);
        double radius = R * sqrt(randomDouble(0, 1));
        Point p;
        p.x = radius * cos(angle);
        p.y = radius * sin(angle);
        points.push_back(p);
    }
    return points;
}

vector<Point> generateRandomPointsOnCircleBorder(int n) {
    vector<Point> points;
    double R = 1'000.0;
    for (int i = 0; i < n; ++i) {
        double angle = randomDouble(0, 2 * M_PI);
        Point p;
        p.x = R * cos(angle);
        p.y = R * sin(angle);
        points.push_back(p);
    }
    return points;
}

vector<Point> generateRandomPointsInRectangle(int n) {
    vector<Point> points;

    double xMin = -1000.0;
    double xMax = 1000.0;
    double yMin = -1000.0;
    double yMax = 1000.0;

    for (int i = 0; i < n; ++i) {
        Point p;
        p.x = randomDouble(xMin, xMax);
        p.y = randomDouble(yMin, yMax);
        points.push_back(p);
    }
    return points;
}

vector<Point> generateRandomPointsOnRectangleBorder(int n) {
    vector<Point> points;

    double xMin = -1'000.0;
    double xMax = 1'000.0;
    double yMin = -1'000.0;
    double yMax = 1'000.0;

    for (int i = 0; i < n; ++i) {
        int edge = rand() % 4;
        Point p;
        switch (edge) {
            case 0: // Top edge
                p.x = randomDouble(xMin, xMax);
                p.y = yMax;
                break;
            case 1: // Bottom edge
                p.x = randomDouble(xMin, xMax);
                p.y = yMin;
                break;
            case 2: // Left edge
                p.x = xMin;
                p.y = randomDouble(yMin, yMax);
                break;
            case 3: // Right edge
                p.x = xMax;
                p.y = randomDouble(yMin, yMax);
                break;
        }
        points.push_back(p);
    }
    return points;
}

// Parabola function y = ax^2 + bx + c
double parabola(double x, double a, double b, double c) {
    return a * x * x + b * x + c;
}

vector<Point> generateRandomPointsInParabolaRegion(int n) {
    vector<Point> points;
    double xMin = -1000.0, xMax = 1000.0;
    double yMin = 0.0;
    double a = 10.0, b = 0.0, c = 0.0;


    for (int i = 0; i < n; ++i) {
        double x = randomDouble(xMin, xMax);
        double yMax = parabola(x, a, b, c);
        double y = randomDouble(yMin, yMax);
        Point p = {x, y};
        points.push_back(p);
    }
    return points;
}

vector<Point> generateRandomPointsOnParabola(int n) {
    vector<Point> points;

    double xMin = -1'000.0, xMax = 1'000.0;
    double yMin = 0.0;
    double a = 10.0, b = 0.0, c = 0.0;

    for (int i = 0; i < n; ++i) {
        double x = randomDouble(xMin, xMax);
        double y = parabola(x, a, b, c);
        Point p = {x, y};
        points.push_back(p);
    }
    return points;
}


// cout << "Random points within the circle:\n";
// for (const auto& p : points) {
//     cout << "(" << p.x << ", " << p.y << ")\n";
// }

template <typename Algorithm, typename Generator>
void testAlgorithm(string name, Algorithm algorithm, string gen_name, Generator generator)
{
    vector<int> npoints = {1'000, 10'000, 100'000, 1'000'000, 2'000'000, 5'000'000};

    for (int n : npoints) {
        vector<Point> points = generator(n);
        auto start = high_resolution_clock::now();
        algorithm(points);
        auto stop = high_resolution_clock::now();
        auto duration = duration_cast<microseconds>(stop - start);
        cout << name << " with " << n << " random points in " << gen_name << " : " << duration.count() << " microseconds" << endl;
    }
}


int main() {

    srand(static_cast<unsigned int>(time(0)));

    /* random points in a circle */
    // testAlgorithm("Jarvis March", jarvisMarch, "a circle", generateRandomPointsInCircle);
    // testAlgorithm("Graham Scan", grahamScan, "a circle", generateRandomPointsInCircle);

    /* random points in the border of a circle */
    // testAlgorithm("Jarvis March", jarvisMarch, "the border of a circle", generateRandomPointsOnCircleBorder);
    // testAlgorithm("Graham Scan", grahamScan, "the border of a circle", generateRandomPointsOnCircleBorder);


    /* random points in a rectangle */
    // testAlgorithm("Jarvis March", jarvisMarch, "a rectangle", generateRandomPointsInRectangle);
    // testAlgorithm("Graham Scan", grahamScan, "a rectangle", generateRandomPointsInRectangle);


    /* random points in the border of a rectangle */
    // testAlgorithm("Jarvis March", jarvisMarch, "the border of a rectangle", generateRandomPointsOnRectangleBorder);
    // testAlgorithm("Graham Scan", grahamScan, "the border of a rectangle", generateRandomPointsOnRectangleBorder);
    
    /* random points inside a region limited by a parabola */
    // testAlgorithm("Jarvis March", jarvisMarch, " a region limited by a parabola", generateRandomPointsInParabolaRegion);
    // testAlgorithm("Graham Scan", grahamScan, " a region limited by a parabola", generateRandomPointsInParabolaRegion);
    
    /* random points on a parabola */
    // testAlgorithm("Jarvis March", jarvisMarch, "a parabol", generateRandomPointsOnParabola);
    // testAlgorithm("Graham Scan", grahamScan, "a parabol", generateRandomPointsOnParabola);

    return 0;
}
