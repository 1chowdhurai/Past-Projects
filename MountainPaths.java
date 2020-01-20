/*
 * Mountain Paths - Greedy Algorithm
 * Mr. Muir
 * 2018.03.26 - v1.0
 */
package edu.hdsb.gwss.rahman.ics4u.u3;

import java.awt.*;
import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;
import java.util.StringTokenizer;

public class MountainPaths {

    static final String FS = File.separator;

    /**
     * Mount Paths
     */
    public static void main(String[] args) throws Exception {

        // ***********************************
        // TASK 1:  read data into a 2D Array
        // 
        System.out.println("TASK 1: READ DATA");
        int[][] data = read("." + FS + "data" + FS + "mountain.paths" + FS + "Colorado.844x480.dat");

        // ***********************************
        // Construct DrawingPanel, and get its Graphics context
        //
        DrawingPanel panel = new DrawingPanel(data[0].length, data.length);
        Graphics g = panel.getGraphics();

        // ***********************************
        // TASK 2:  find HIGHEST & LOWEST elevation; for GRAY SCALE
        //
        System.out.println("TASK 2: HIGHEST / LOWEST ELEVATION");
        int min = findMinValue(data);
        System.out.println("\tMin: " + min);

        int max = findMaxValue(data);
        System.out.println("\tMax: " + max);

        // ***********************************
        // TASK 3:  Draw The Map
        //
        System.out.println("TASK 3: DRAW MAP");
        drawMap(g, data);

        // ***********************************
        // TASK 4A:  implement indexOfMinInCol
        //
        System.out.println("TASK 4A: INDEX OF MIN IN COL 0");
        int minRow = indexOfMinInCol(data, 0);
        System.out.println("\tRow with lowest Col 0 Value: " + minRow);

        // ***********************************
        // TASK 4B:  use minRow as starting point to draw path
        //
        System.out.println("TASK 4B: PATH from LOWEST STARTING ELEVATION");
        g.setColor(Color.RED);
        int totalChange = drawLowestElevPath(g, data, minRow, 0); //
        System.out.println("\tLowest-Elevation-Change Path starting at row " + minRow + " gives total change of: " + totalChange);

        // ***********************************
        // TASK 5:  determine the BEST path
        //
        g.setColor(Color.RED);
        int bestRow = indexOfLowestElevPath(g, data);
        System.out.println("Best Row : " + bestRow);

        // ***********************************
        // TASK 6:  draw the best path
        //
        System.out.println("TASK 6: DRAW BEST PATH");
        //drawMap(g,data); //use this to get rid of all red lines
        g.setColor(Color.GREEN); //set brush to green for drawing best path
        totalChange = drawLowestElevPath(g, data, bestRow, 0);
        System.out.println("\tThe Lowest-Elevation-Change Path starts at row: " + bestRow + " and gives a total change of: " + totalChange);
    }

    /**
     * This method reads a 2D data set from the specified file. The Graphics'
     * industry standard is width by height (width x height), while programmers
     * use rows x cols / (height x width).
     *
     * @param fileName the name of the file
     * @return a 2D array (rows x cols) of the data from the file read
     */
    public static int[][] read(String fileName) throws FileNotFoundException {
        //variables
        int[][] data = null;
        File file = new File(fileName);
        Scanner determineFileLength = new Scanner(file);
        Scanner dataCollector = new Scanner(file);

        //first go through file and store number of columns
        StringTokenizer st = new StringTokenizer(determineFileLength.nextLine());
        int col = 0;
        while (st.hasMoreTokens()) {
            col++;
            st.nextToken();
        }
        
        //go through file and store number of rows
        int rows = 1;
        while (determineFileLength.hasNextLine()) {
            rows++;
            determineFileLength.nextLine();
        }

        
        //read through file and store all data
        data = new int[rows][col];

        for (int i = 0; i < rows; i++) {
            st = new StringTokenizer(dataCollector.nextLine());
            for (int j = 0; j < col; j++) {
                data[i][j] = Integer.parseInt(st.nextToken());

            }

        }

        // TODO
        return data;
    }

    /**
     * @param grid a 2D array from which you want to find the smallest value
     * @return the smallest value in the given 2D array
     */
    public static int findMinValue(int[][] grid) {
        //loop through all the data and determine the minimum value
        int min = grid[0][0];
        for (int i = 0; i < grid.length; i++) {
            for (int j = 0; j < grid[i].length; j++) {
                if (grid[i][j] < min) {
                    min = grid[i][j];
                }
            }
        }

        return min;

    }

    /**
     * @param grid a 2D array from which you want to find the largest value
     * @return the largest value in the given 2D array
     */
    public static int findMaxValue(int[][] grid) {
        //loop through all the data and determine the maximum value
        int max = grid[0][0];
        for (int i = 0; i < grid.length; i++) {
            for (int j = 0; j < grid[i].length; j++) {
                if (grid[i][j] > max) {
                    max = grid[i][j];
                }
            }
        }

        return max;

    }

    /**
     * Given a 2D array of elevation data create a image of size rows x cols,
     * drawing a 1x1 rectangle for each value in the array whose color is set to
     * a a scaled gray value (0-255). Note: to scale the values in the array to
     * 0-255 you must find the min and max values in the original data first.
     *
     * @param g a Graphics context to use
     * @param grid a 2D array of the data
     */
    public static void drawMap(Graphics g, int[][] data) {
        
        //variables
        int min = findMinValue(data);
        int max = findMaxValue(data);

        double m = 255.0 / (max - min);
        int b = (int) (m * min);
        int c;

        //loop through every pixel and determine the grey scale
        for (int i = 0; i < data.length; i++) {
            for (int j = 0; j < data[i].length; j++) {
                //linear equation to determine the grey scale
                c = (int) (m * data[i][j] - b);
                //sets the colour and fills the pixel
                g.setColor(new Color(c, c, c));
                g.fillRect(j, i, 1, 1);
            }
        }

    }

    /**
     * Scan a single column of a 2D array and return the index of the row that
     * contains the smallest value
     *
     * @param grid a 2D array
     * @col the column in the 2D array to process
     * @return the index of smallest value from grid at the given col
     */
    public static int indexOfMinInCol(int[][] grid, int col) {
        
        //loops through the first column and stores the index of the minimum row
        int min = grid[0][col];
        int minIndex = 0;
        for (int i = 1; i < grid.length; i++) {
            if (grid[i][col] < min) {
                min = grid[i][col];
                minIndex = i;
            }
        }
        return minIndex;
    }

    /**
     * Find the minimum elevation-change route from West-to-East in the given
     * grid, from the given starting row, and draw it using the given graphics
     * context
     *
     * @param g - the graphics context to use
     * @param grid - the 2D array of elevation values
     * @param row - the starting row for traversing to find the min path
     * @return total elevation of the route
     */
    public static int drawLowestElevPath(Graphics g, int[][] data, int row, int col) {
        //marks which pixel it's on
        g.fillRect(col, row, 1, 1);

        
        //base case: if you're at the end, there's no more elevation change
        if (col == data[row].length - 1) {
            return 0;
        }

        //variables for the elevation change for top, middle and bottom path
        int topDiff;        
        int midDiff = Math.abs(data[row][col + 1] - data[row][col]);
        int botDiff;
        
        //if its at the top row, set the top elevation change to be the max integer value
        //so it never chooses the top
        if (row == 0) {
            topDiff = Integer.MAX_VALUE;
        }
        
        //otherwise calculate the value
        else{
            topDiff = Math.abs(data[row - 1][col + 1] - data[row][col]);
        }
        //same if it's at the bottom row, set botDiff to be max integer value so it never chooses 
        //the bottom
        if (row == data.length - 1) {
            botDiff = Integer.MAX_VALUE;
        }
        //otherwise calculate the value
        else{
            botDiff = Math.abs(data[row + 1][col + 1] - data[row][col]);
        }
        
        //take top row
        if (topDiff < midDiff && topDiff < botDiff) {
            return topDiff + drawLowestElevPath(g, data, row - 1, col + 1);
        }
        //take middle row
        if (midDiff < topDiff && midDiff < botDiff) {
            return midDiff + drawLowestElevPath(g, data, row, col + 1);
        }
        //take bottom row
        if (botDiff < midDiff && botDiff < topDiff) {
            return botDiff + drawLowestElevPath(g, data, row + 1, col + 1);
        }
        //otherwise, if there's a tie between middle and another row, always take the middle
        if (midDiff == topDiff || midDiff == botDiff) {
            return midDiff + drawLowestElevPath(g, data, row, col + 1);
        }
        
        //otherwise if there's a tie between top and bottom, flip a coin
        int random = (int) (Math.random() * 2);
        if (random == 0) {
            return topDiff + drawLowestElevPath(g, data, row - 1, col + 1);
        }
        return botDiff + drawLowestElevPath(g, data, row + 1, col + 1);

    }

    /**
     * Generate all west-to-east paths, find the one with the lowest total
     * elevation change, and return the index of the row that path starts on.
     *
     * @param g - the graphics context to use
     * @param grid - the 2D array of elevation values
     * @return the index of the row where the lowest elevation-change path
     * starts.
     */
    public static int indexOfLowestElevPath(Graphics g, int[][] data) {

        //loops through every single row and determines the index of the path with the lowest 
        //elevation change
        int min = drawLowestElevPath(g, data, 0, 0);
        int changeInElevation;
        int minRow = 0;
        for (int i = 1; i < data.length; i++) {
            changeInElevation = drawLowestElevPath(g, data, i, 0);

            if (changeInElevation < min) {
                min = changeInElevation;
                minRow = i;

            }

        }
        return minRow;
    }

}
