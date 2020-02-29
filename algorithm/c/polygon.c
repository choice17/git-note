#include <stdio.h>
#include <stdlib.h>

typedef enum {
    UNKNOWN=-1,
    CONVEX,
    CONCAVE,
    COMPLEX
} POLY_SHAPE_E;

typedef struct {
    int x;
    int y;
} PT_S;

typedef struct {
    PT_S *pts;
    int num;
} POLY_S;


POLY_SHAPE_E poly_check(const POLY_S *poly);
int poly_area(const POLY_S *poly);
void poly_clip(const POLY_S *src, const POLY_S *clipper, POLY_S *dst);
void poly_fill(const POLY_S *poly, unsigned char *data, int w, int h, unsigned char color);

void poly_fill(const POLY_S *poly, unsigned char *data, int w, int h, unsigned char color);
{
    return;
}

/* Sutherland-Hodgman algorithm */
void poly_clip(const POLY_S *src, const POLY_S *clipper, POLY_S *dst);
{
    return;
}

/* Not working */
POLY_SHAPE poly_check(const POLY_S *poly)
{
    int i;
    int dx1, dy1, dx2, dy2, sign = 0, tmp_sign, z_cross_product;
    if (poly->num < 3) return UNKNOWN;
    if (poly->num == 3) return CONVEX;
    for (i = 0; i < poly->num-2; i++) {
        dx1 = poly->pts[i+1].x-poly->pts[i].x;
        dy1 = poly->pts[i+1].y-poly->pts[i].y;
        dx2 = poly->pts[i+2].x-poly->pts[i+1].x;
        dy2 = poly->pts[i+2].y-poly->pts[i+1].y;
        z_cross_product = dx1 * dx2 - dy1 * dy2;
        tmp_sign = ((z_cross_product) >= 0)? 1 : -1;
        if (sign == 0) {
            sign = tmp_sign;
        } else {
            if (sign != tmp_sign)
                return CONCAVE;
        }
    }
    return CONVEX;
}

/**
 *@brief Shoelace formula for polygon area
 *
 **/
int poly_area(const POLY_S *poly)
{
    int i;
    int area = 0;
    for (i = 0; i < poly->num-1; i++) {
        area += poly->pts[i].x * poly->pts[i+1].y;
    }
    area += poly->pts[i].x * poly->pts[0].y;
    for (i = 0; i < poly->num-1; i++) {
        area -= poly->pts[i+1].x * poly->pts[i].y;
    }
    area -= poly->pts[0].x * poly->pts[i].y;
    return area / 2;
}

int main(void)
{
    POLY_S poly = {
        .num = 5,
        .pts = NULL
    };
    poly.pts = malloc(sizeof(PT_S)*poly.num);
    poly.pts[0].x = 0;
    poly.pts[0].y = 0;
    poly.pts[1].x = 200;
    poly.pts[1].y = 0;
    poly.pts[2].x = 100;
    poly.pts[2].y = 100;
    poly.pts[3].x = 0;
    poly.pts[3].y = 100;
    poly.pts[4].x = -50;
    poly.pts[4].y = -50;
    int area = poly_area(&poly);
    printf("%d\n", area);
    return 0;
}