/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package edu.hdsb.gwss.rahman.ics4u.u2;

import java.awt.Color;
import java.awt.event.KeyEvent;
import javax.swing.JLabel;

/**
 *
 * @author 1chowdhurai
 */
public class Game2048 extends javax.swing.JFrame {

    private int[][] data;
    private JLabel[][] jLabels;
    private int score;
    private boolean gameOver,win;

    public Game2048() {
        initComponents();
        this.data = new int[4][4];
        this.jLabels = new JLabel[4][4];

        //row 0
        jLabels[0][0] = jLabel00;
        jLabels[0][1] = jLabel01;
        jLabels[0][2] = jLabel02;
        jLabels[0][3] = jLabel03;

        //row 1
        jLabels[1][0] = jLabel10;
        jLabels[1][1] = jLabel11;
        jLabels[1][2] = jLabel12;
        jLabels[1][3] = jLabel13;

        //row 2
        jLabels[2][0] = jLabel20;
        jLabels[2][1] = jLabel21;
        jLabels[2][2] = jLabel22;
        jLabels[2][3] = jLabel23;

        //row 3
        jLabels[3][0] = jLabel30;
        jLabels[3][1] = jLabel31;
        jLabels[3][2] = jLabel32;
        jLabels[3][3] = jLabel33;

        score = 0;
        gameOver = false;
        win = false;

        placeRandomeTwo();
        placeRandomeTwo();

        updateGameBoard();
        
    }

    private static final Color[] COLOUR_BG = {
        new Color(205, 193, 180), // 0
        new Color(238, 228, 218), // 2
        new Color(237, 224, 200), // 4
        new Color(242, 177, 121), // 8
        new Color(245, 149, 99), // 16
        new Color(245, 149, 99), // 32
        new Color(246, 94, 59), // 64
        new Color(246, 94, 59), // 128
        new Color(237, 204, 97), // 256
        new Color(237, 204, 97), // 512
        new Color(237, 204, 97), // 1024
        new Color(237, 204, 97) // 2048
    };
    private static final Color[] COLOUR_FONT = {
        new Color(205, 193, 180), // 0
        new Color(119, 110, 101), // 2
        new Color(119, 110, 101), // 4
        new Color(249, 246, 242), // 8
        new Color(249, 246, 242), // 16
        new Color(249, 246, 242), // 32
        new Color(249, 246, 242), // 64
        new Color(249, 246, 242), // 128
        new Color(249, 246, 242), // 256
        new Color(249, 246, 242), // 512
        new Color(249, 246, 242), // 1024
        new Color(249, 246, 242) // 2048
    };

    public void placeRandomeTwo() {
        boolean occupied = true;
        int row;
        int col;

        while (occupied) {
            row = (int) (Math.random() * data.length);
            col = (int) (Math.random() * data[0].length);
            int num = 2;
            if (Math.random() > 0.8) {
                num = 4;
            }
            if (data[row][col] == 0) {
                data[row][col] = num;
                occupied = false;
            }
        }
    }

    public void updateGameBoard() {
        int colourIndex;
        for (int i = 0; i < data.length; i++) {
            for (int j = 0; j < data[i].length; j++) {

                // COLOUR BASED ON VALUE
                if (data[i][j] == 0) {
                    colourIndex = 0;
                } else {
                    colourIndex = (int) (Math.log(data[i][j]) / Math.log(2));
                }
                this.jLabels[i][j].setBackground(COLOUR_BG[colourIndex]);
                this.jLabels[i][j].setForeground(COLOUR_FONT[colourIndex]);
                this.jLabels[i][j].setText("" + this.data[i][j]);
            }
        }
    }

    public boolean checkGameOver() {
        boolean allFull = true;
        boolean gameOver = true;
        for (int i = 0; i < data.length; i++) {
            for (int j = 0; j < data[i].length; j++) {
                if (data[i][j] == 0) {
                    allFull = false;
                }
            }
        }
        if (allFull) {
            for (int i = 0; i < data.length; i++) {
                for (int j = 0; j < data[i].length; j++) {
                    try {
                        if (data[i][j + 1] == data[i][j]) {
                            gameOver = false;
                        }
                    } catch (Exception ignore) {

                    }
                    try {
                        if (data[i][j - 1] == data[i][j]) {
                            gameOver = false;
                        }

                    } catch (Exception ignore) {

                    }
                    try {
                        if (data[i + 1][j] == data[i][j]) {
                            gameOver = false;
                        }
                    } catch (Exception ignore) {

                    }
                    try {
                        if (data[i - 1][j] == data[i][j]) {
                            gameOver = false;
                        }
                    } catch (Exception ignore) {

                    }
                }
            }
        } else {
            gameOver = false;
        }
        return gameOver;
    }

    public boolean checkWin() {
        boolean win = false;
        for (int i = 0; i < data.length; i++) {
            for (int j = 0; j < data[i].length; j++) {
                if (data[i][j] == 2048) {
                    win = true;
                }
            }
        }
        return win;
    }

    public boolean shiftLeft() {
        boolean shifted = false;
        for (int i = 0; i < data.length; i++) {
            for (int pass = 0; pass < data[i].length - 1; pass++) {
                for (int j = 1; j < data[i].length; j++) {

                    if (data[i][j] != 0 && data[i][j - 1] == 0) {

                        data[i][j - 1] = data[i][j];
                        data[i][j] = 0;
                        shifted = true;

                    }
                }
            }
        }
        return shifted;
    }

    public boolean mergeLeft() {
        boolean merged = false;
        for (int i = 0; i < data.length; i++) {
            for (int j = 1; j < data[i].length; j++) {
                if (data[i][j] == data[i][j - 1] && data[i][j] != 0) {

                    data[i][j - 1] *= 2;
                    data[i][j] = 0;
                    merged = true;
                    score += data[i][j - 1];

                }
            }
        }
        return merged;
    }

    public boolean shiftUp() {
        boolean shifted = false;
        for (int i = 0; i < data.length; i++) {
            for (int pass = 0; pass < data.length - 1; pass++) {
                for (int j = 1; j < data[i].length; j++) {

                    if (data[j][i] != 0 && data[j - 1][i] == 0) {

                        data[j - 1][i] = data[j][i];
                        data[j][i] = 0;
                        shifted = true;

                    }
                }
            }
        }
        return shifted;
    }

    public boolean mergeUp() {
        boolean merged = false;
        for (int i = 0; i < data.length; i++) {
            for (int j = 1; j < data[i].length; j++) {
                if (data[j][i] == data[j - 1][i] && data[j][i] != 0) {

                    data[j - 1][i] *= 2;
                    data[j][i] = 0;
                    merged = true;
                    score += data[j - 1][i];

                }
            }
        }
        return merged;
    }

    public boolean shiftRight() {
        boolean shifted = false;
        for (int i = 0; i < data.length; i++) {
            for (int pass = 0; pass < data.length - 1; pass++) {
                for (int j = data[i].length - 1; j > 0; j--) {

                    if (data[i][j - 1] != 0 && data[i][j] == 0) {
                        data[i][j] = data[i][j - 1];
                        data[i][j - 1] = 0;
                        shifted = true;

                    }
                }
            }
        }
        return shifted;
    }

    public boolean mergeRight() {
        boolean merged = false;
        for (int i = 0; i < data.length; i++) {
            for (int j = data[i].length - 1; j > 0; j--) {
                if (data[i][j] == data[i][j - 1] && data[i][j] != 0) {

                    data[i][j] *= 2;
                    data[i][j - 1] = 0;
                    merged = true;
                    score += data[i][j];

                }
            }
        }
        return merged;
    }

    public boolean shiftDown() {
        boolean shifted = false;
        for (int i = 0; i < data.length; i++) {
            for (int pass = 0; pass < data.length - 1; pass++) {
                for (int j = data[i].length - 1; j > 0; j--) {

                    if (data[j - 1][i] != 0 && data[j][i] == 0) {
                        data[j][i] = data[j - 1][i];
                        data[j - 1][i] = 0;
                        shifted = true;

                    }
                }
            }
        }
        return shifted;
    }

    public boolean mergeDown() {
        boolean merged = false;
        for (int i = 0; i < data.length; i++) {
            for (int j = data[i].length - 1; j > 0; j--) {
                if (data[j][i] == data[j - 1][i] && data[j][i] != 0) {

                    data[j][i] *= 2;
                    data[j - 1][i] = 0;
                    merged = true;
                    score += data[j][i];

                }
            }
        }
        return merged;
    }

    /**
     * This method is called from within the constructor to initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is always
     * regenerated by the Form Editor.
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        jPanelTop = new javax.swing.JPanel();
        jLabel1 = new javax.swing.JLabel();
        jPanelMiddle = new javax.swing.JPanel();
        jLabelScore = new javax.swing.JLabel();
        jLabelScoreNum = new javax.swing.JLabel();
        jLabelGameOver = new javax.swing.JLabel();
        jPanelBottom = new javax.swing.JPanel();
        jLabel00 = new javax.swing.JLabel();
        jLabel31 = new javax.swing.JLabel();
        jLabel21 = new javax.swing.JLabel();
        jLabel10 = new javax.swing.JLabel();
        jLabel20 = new javax.swing.JLabel();
        jLabel30 = new javax.swing.JLabel();
        jLabel11 = new javax.swing.JLabel();
        jLabel01 = new javax.swing.JLabel();
        jLabel32 = new javax.swing.JLabel();
        jLabel13 = new javax.swing.JLabel();
        jLabel03 = new javax.swing.JLabel();
        jLabel02 = new javax.swing.JLabel();
        jLabel33 = new javax.swing.JLabel();
        jLabel23 = new javax.swing.JLabel();
        jLabel12 = new javax.swing.JLabel();
        jLabel22 = new javax.swing.JLabel();

        setDefaultCloseOperation(javax.swing.WindowConstants.EXIT_ON_CLOSE);
        addKeyListener(new java.awt.event.KeyAdapter() {
            public void keyPressed(java.awt.event.KeyEvent evt) {
                formKeyPressed(evt);
            }
        });

        jPanelTop.setBackground(new java.awt.Color(243, 240, 189));

        jLabel1.setFont(new java.awt.Font("Tahoma", 1, 48)); // NOI18N
        jLabel1.setText("2048");

        javax.swing.GroupLayout jPanelTopLayout = new javax.swing.GroupLayout(jPanelTop);
        jPanelTop.setLayout(jPanelTopLayout);
        jPanelTopLayout.setHorizontalGroup(
            jPanelTopLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, jPanelTopLayout.createSequentialGroup()
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                .addComponent(jLabel1)
                .addGap(119, 119, 119))
        );
        jPanelTopLayout.setVerticalGroup(
            jPanelTopLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, jPanelTopLayout.createSequentialGroup()
                .addContainerGap(34, Short.MAX_VALUE)
                .addComponent(jLabel1)
                .addGap(31, 31, 31))
        );

        jPanelMiddle.setBackground(new java.awt.Color(255, 224, 198));

        jLabelScore.setText("Score:");

        jLabelScoreNum.setText("0");

        jLabelGameOver.setFont(new java.awt.Font("Comic Sans MS", 0, 18)); // NOI18N

        javax.swing.GroupLayout jPanelMiddleLayout = new javax.swing.GroupLayout(jPanelMiddle);
        jPanelMiddle.setLayout(jPanelMiddleLayout);
        jPanelMiddleLayout.setHorizontalGroup(
            jPanelMiddleLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(jPanelMiddleLayout.createSequentialGroup()
                .addContainerGap()
                .addComponent(jLabelScore)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                .addComponent(jLabelScoreNum)
                .addGap(55, 55, 55)
                .addComponent(jLabelGameOver, javax.swing.GroupLayout.PREFERRED_SIZE, 109, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
        );
        jPanelMiddleLayout.setVerticalGroup(
            jPanelMiddleLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(jPanelMiddleLayout.createSequentialGroup()
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                .addGroup(jPanelMiddleLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(jLabelScore)
                    .addComponent(jLabelScoreNum))
                .addGap(40, 40, 40))
            .addGroup(jPanelMiddleLayout.createSequentialGroup()
                .addGap(24, 24, 24)
                .addComponent(jLabelGameOver, javax.swing.GroupLayout.PREFERRED_SIZE, 46, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addContainerGap(30, Short.MAX_VALUE))
        );

        jPanelBottom.setBackground(new java.awt.Color(187, 173, 160));

        jLabel00.setFont(new java.awt.Font("Comic Sans MS", 1, 24)); // NOI18N
        jLabel00.setHorizontalAlignment(javax.swing.SwingConstants.CENTER);
        jLabel00.setText("0,0");
        jLabel00.setMaximumSize(new java.awt.Dimension(35, 35));
        jLabel00.setMinimumSize(new java.awt.Dimension(35, 35));
        jLabel00.setOpaque(true);
        jLabel00.setPreferredSize(new java.awt.Dimension(35, 35));

        jLabel31.setFont(new java.awt.Font("Comic Sans MS", 1, 24)); // NOI18N
        jLabel31.setHorizontalAlignment(javax.swing.SwingConstants.CENTER);
        jLabel31.setText("3,1");
        jLabel31.setMaximumSize(new java.awt.Dimension(35, 35));
        jLabel31.setMinimumSize(new java.awt.Dimension(35, 35));
        jLabel31.setOpaque(true);
        jLabel31.setPreferredSize(new java.awt.Dimension(35, 35));

        jLabel21.setFont(new java.awt.Font("Comic Sans MS", 1, 24)); // NOI18N
        jLabel21.setHorizontalAlignment(javax.swing.SwingConstants.CENTER);
        jLabel21.setText("2,1");
        jLabel21.setMaximumSize(new java.awt.Dimension(35, 35));
        jLabel21.setMinimumSize(new java.awt.Dimension(35, 35));
        jLabel21.setOpaque(true);
        jLabel21.setPreferredSize(new java.awt.Dimension(35, 35));

        jLabel10.setFont(new java.awt.Font("Comic Sans MS", 1, 24)); // NOI18N
        jLabel10.setHorizontalAlignment(javax.swing.SwingConstants.CENTER);
        jLabel10.setText("1,0");
        jLabel10.setMaximumSize(new java.awt.Dimension(35, 35));
        jLabel10.setMinimumSize(new java.awt.Dimension(35, 35));
        jLabel10.setOpaque(true);
        jLabel10.setPreferredSize(new java.awt.Dimension(35, 35));

        jLabel20.setFont(new java.awt.Font("Comic Sans MS", 1, 24)); // NOI18N
        jLabel20.setHorizontalAlignment(javax.swing.SwingConstants.CENTER);
        jLabel20.setText("2,0");
        jLabel20.setMaximumSize(new java.awt.Dimension(35, 35));
        jLabel20.setMinimumSize(new java.awt.Dimension(35, 35));
        jLabel20.setOpaque(true);
        jLabel20.setPreferredSize(new java.awt.Dimension(35, 35));

        jLabel30.setFont(new java.awt.Font("Comic Sans MS", 1, 24)); // NOI18N
        jLabel30.setHorizontalAlignment(javax.swing.SwingConstants.CENTER);
        jLabel30.setText("3,0");
        jLabel30.setMaximumSize(new java.awt.Dimension(35, 35));
        jLabel30.setMinimumSize(new java.awt.Dimension(35, 35));
        jLabel30.setOpaque(true);
        jLabel30.setPreferredSize(new java.awt.Dimension(35, 35));

        jLabel11.setFont(new java.awt.Font("Comic Sans MS", 1, 24)); // NOI18N
        jLabel11.setHorizontalAlignment(javax.swing.SwingConstants.CENTER);
        jLabel11.setText("1,1");
        jLabel11.setMaximumSize(new java.awt.Dimension(35, 35));
        jLabel11.setMinimumSize(new java.awt.Dimension(35, 35));
        jLabel11.setOpaque(true);
        jLabel11.setPreferredSize(new java.awt.Dimension(35, 35));

        jLabel01.setFont(new java.awt.Font("Comic Sans MS", 1, 24)); // NOI18N
        jLabel01.setHorizontalAlignment(javax.swing.SwingConstants.CENTER);
        jLabel01.setText("0,1");
        jLabel01.setMaximumSize(new java.awt.Dimension(35, 35));
        jLabel01.setMinimumSize(new java.awt.Dimension(35, 35));
        jLabel01.setOpaque(true);
        jLabel01.setPreferredSize(new java.awt.Dimension(35, 35));

        jLabel32.setFont(new java.awt.Font("Comic Sans MS", 1, 24)); // NOI18N
        jLabel32.setHorizontalAlignment(javax.swing.SwingConstants.CENTER);
        jLabel32.setText("3,2");
        jLabel32.setMaximumSize(new java.awt.Dimension(35, 35));
        jLabel32.setMinimumSize(new java.awt.Dimension(35, 35));
        jLabel32.setOpaque(true);
        jLabel32.setPreferredSize(new java.awt.Dimension(35, 35));

        jLabel13.setFont(new java.awt.Font("Comic Sans MS", 1, 24)); // NOI18N
        jLabel13.setHorizontalAlignment(javax.swing.SwingConstants.CENTER);
        jLabel13.setText("1,3");
        jLabel13.setMaximumSize(new java.awt.Dimension(35, 35));
        jLabel13.setMinimumSize(new java.awt.Dimension(35, 35));
        jLabel13.setOpaque(true);
        jLabel13.setPreferredSize(new java.awt.Dimension(35, 35));

        jLabel03.setFont(new java.awt.Font("Comic Sans MS", 1, 24)); // NOI18N
        jLabel03.setHorizontalAlignment(javax.swing.SwingConstants.CENTER);
        jLabel03.setText("0,3");
        jLabel03.setMaximumSize(new java.awt.Dimension(35, 35));
        jLabel03.setMinimumSize(new java.awt.Dimension(35, 35));
        jLabel03.setOpaque(true);
        jLabel03.setPreferredSize(new java.awt.Dimension(35, 35));

        jLabel02.setFont(new java.awt.Font("Comic Sans MS", 1, 24)); // NOI18N
        jLabel02.setHorizontalAlignment(javax.swing.SwingConstants.CENTER);
        jLabel02.setText("0,2");
        jLabel02.setMaximumSize(new java.awt.Dimension(35, 35));
        jLabel02.setMinimumSize(new java.awt.Dimension(35, 35));
        jLabel02.setOpaque(true);
        jLabel02.setPreferredSize(new java.awt.Dimension(35, 35));

        jLabel33.setFont(new java.awt.Font("Comic Sans MS", 1, 24)); // NOI18N
        jLabel33.setHorizontalAlignment(javax.swing.SwingConstants.CENTER);
        jLabel33.setText("3,3");
        jLabel33.setMaximumSize(new java.awt.Dimension(35, 35));
        jLabel33.setMinimumSize(new java.awt.Dimension(35, 35));
        jLabel33.setOpaque(true);
        jLabel33.setPreferredSize(new java.awt.Dimension(35, 35));

        jLabel23.setFont(new java.awt.Font("Comic Sans MS", 1, 24)); // NOI18N
        jLabel23.setHorizontalAlignment(javax.swing.SwingConstants.CENTER);
        jLabel23.setText("2,3");
        jLabel23.setMaximumSize(new java.awt.Dimension(35, 35));
        jLabel23.setMinimumSize(new java.awt.Dimension(35, 35));
        jLabel23.setOpaque(true);
        jLabel23.setPreferredSize(new java.awt.Dimension(35, 35));

        jLabel12.setFont(new java.awt.Font("Comic Sans MS", 1, 24)); // NOI18N
        jLabel12.setHorizontalAlignment(javax.swing.SwingConstants.CENTER);
        jLabel12.setText("1,2");
        jLabel12.setMaximumSize(new java.awt.Dimension(35, 35));
        jLabel12.setMinimumSize(new java.awt.Dimension(35, 35));
        jLabel12.setOpaque(true);
        jLabel12.setPreferredSize(new java.awt.Dimension(35, 35));

        jLabel22.setFont(new java.awt.Font("Comic Sans MS", 1, 24)); // NOI18N
        jLabel22.setHorizontalAlignment(javax.swing.SwingConstants.CENTER);
        jLabel22.setText("2,2");
        jLabel22.setMaximumSize(new java.awt.Dimension(35, 35));
        jLabel22.setMinimumSize(new java.awt.Dimension(35, 35));
        jLabel22.setOpaque(true);
        jLabel22.setPreferredSize(new java.awt.Dimension(35, 35));

        javax.swing.GroupLayout jPanelBottomLayout = new javax.swing.GroupLayout(jPanelBottom);
        jPanelBottom.setLayout(jPanelBottomLayout);
        jPanelBottomLayout.setHorizontalGroup(
            jPanelBottomLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(jPanelBottomLayout.createSequentialGroup()
                .addContainerGap()
                .addGroup(jPanelBottomLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(jPanelBottomLayout.createSequentialGroup()
                        .addComponent(jLabel00, javax.swing.GroupLayout.PREFERRED_SIZE, 70, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addGap(18, 18, 18)
                        .addComponent(jLabel01, javax.swing.GroupLayout.PREFERRED_SIZE, 70, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addGap(18, 18, 18)
                        .addComponent(jLabel02, javax.swing.GroupLayout.PREFERRED_SIZE, 70, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addGap(18, 18, 18)
                        .addComponent(jLabel03, javax.swing.GroupLayout.PREFERRED_SIZE, 70, javax.swing.GroupLayout.PREFERRED_SIZE))
                    .addGroup(jPanelBottomLayout.createSequentialGroup()
                        .addComponent(jLabel10, javax.swing.GroupLayout.PREFERRED_SIZE, 70, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addGap(18, 18, 18)
                        .addComponent(jLabel11, javax.swing.GroupLayout.PREFERRED_SIZE, 70, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addGap(18, 18, 18)
                        .addComponent(jLabel12, javax.swing.GroupLayout.PREFERRED_SIZE, 70, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addGap(18, 18, 18)
                        .addComponent(jLabel13, javax.swing.GroupLayout.PREFERRED_SIZE, 70, javax.swing.GroupLayout.PREFERRED_SIZE))
                    .addGroup(jPanelBottomLayout.createSequentialGroup()
                        .addComponent(jLabel20, javax.swing.GroupLayout.PREFERRED_SIZE, 70, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addGap(18, 18, 18)
                        .addComponent(jLabel21, javax.swing.GroupLayout.PREFERRED_SIZE, 70, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addGap(18, 18, 18)
                        .addComponent(jLabel22, javax.swing.GroupLayout.PREFERRED_SIZE, 70, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addGap(18, 18, 18)
                        .addComponent(jLabel23, javax.swing.GroupLayout.PREFERRED_SIZE, 70, javax.swing.GroupLayout.PREFERRED_SIZE))
                    .addGroup(jPanelBottomLayout.createSequentialGroup()
                        .addComponent(jLabel30, javax.swing.GroupLayout.PREFERRED_SIZE, 70, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addGap(18, 18, 18)
                        .addComponent(jLabel31, javax.swing.GroupLayout.PREFERRED_SIZE, 70, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addGap(18, 18, 18)
                        .addComponent(jLabel32, javax.swing.GroupLayout.PREFERRED_SIZE, 70, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addGap(18, 18, 18)
                        .addComponent(jLabel33, javax.swing.GroupLayout.PREFERRED_SIZE, 70, javax.swing.GroupLayout.PREFERRED_SIZE)))
                .addContainerGap(19, Short.MAX_VALUE))
        );
        jPanelBottomLayout.setVerticalGroup(
            jPanelBottomLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(jPanelBottomLayout.createSequentialGroup()
                .addContainerGap()
                .addGroup(jPanelBottomLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(jLabel00, javax.swing.GroupLayout.PREFERRED_SIZE, 70, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(jLabel01, javax.swing.GroupLayout.PREFERRED_SIZE, 70, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(jLabel02, javax.swing.GroupLayout.PREFERRED_SIZE, 70, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(jLabel03, javax.swing.GroupLayout.PREFERRED_SIZE, 70, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                .addGroup(jPanelBottomLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(jLabel10, javax.swing.GroupLayout.PREFERRED_SIZE, 70, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(jLabel11, javax.swing.GroupLayout.PREFERRED_SIZE, 70, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(jLabel12, javax.swing.GroupLayout.PREFERRED_SIZE, 70, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(jLabel13, javax.swing.GroupLayout.PREFERRED_SIZE, 70, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                .addGroup(jPanelBottomLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(jLabel20, javax.swing.GroupLayout.PREFERRED_SIZE, 70, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(jLabel21, javax.swing.GroupLayout.PREFERRED_SIZE, 70, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(jLabel22, javax.swing.GroupLayout.PREFERRED_SIZE, 70, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(jLabel23, javax.swing.GroupLayout.PREFERRED_SIZE, 70, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                .addGroup(jPanelBottomLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(jLabel30, javax.swing.GroupLayout.PREFERRED_SIZE, 70, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(jLabel31, javax.swing.GroupLayout.PREFERRED_SIZE, 70, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(jLabel32, javax.swing.GroupLayout.PREFERRED_SIZE, 70, javax.swing.GroupLayout.PREFERRED_SIZE)
                    .addComponent(jLabel33, javax.swing.GroupLayout.PREFERRED_SIZE, 70, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
        );

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(getContentPane());
        getContentPane().setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addComponent(jPanelTop, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
            .addComponent(jPanelMiddle, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
            .addComponent(jPanelBottom, javax.swing.GroupLayout.Alignment.TRAILING, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addComponent(jPanelTop, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(jPanelMiddle, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(jPanelBottom, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
        );

        pack();
    }// </editor-fold>//GEN-END:initComponents

    private void formKeyPressed(java.awt.event.KeyEvent evt) {//GEN-FIRST:event_formKeyPressed
        
        if (!gameOver) {

            boolean shifted = false;
            boolean merged = false;
            switch (evt.getKeyCode()) {
                case KeyEvent.VK_UP:
                    shifted = shiftUp();
                    merged = mergeUp();
                    shifted = shiftUp() || shifted;

                    break;
                case KeyEvent.VK_DOWN:
                    shifted = shiftDown();
                    merged = mergeDown();
                    shifted = shiftDown() || shifted;

                    break;
                case KeyEvent.VK_LEFT:
                    shifted = shiftLeft();
                    merged = mergeLeft();
                    shifted = shiftLeft() || shifted;

                    break;
                case KeyEvent.VK_RIGHT:
                    shifted = shiftRight();
                    merged = mergeRight();
                    shifted = shiftRight() || shifted;

                    break;
            }

            if (shifted || merged) {
                placeRandomeTwo();
                gameOver = checkGameOver();
                if (merged) {
                    jLabelScoreNum.setText(score + "");
                    if(checkWin()){
                        win = true;
                        gameOver = true;
                    }
                }
                
                updateGameBoard();
            }

        }
        if (gameOver && !win) {
            jLabelGameOver.setText("GAME OVER");
        }
        if(win && gameOver){
            jLabelGameOver.setText("You Won!");
        }


    }//GEN-LAST:event_formKeyPressed

    /**
     * @param args the command line arguments
     */
    public static void main(String args[]) {
        /* Set the Nimbus look and feel */
        //<editor-fold defaultstate="collapsed" desc=" Look and feel setting code (optional) ">
        /* If Nimbus (introduced in Java SE 6) is not available, stay with the default look and feel.
         * For details see http://download.oracle.com/javase/tutorial/uiswing/lookandfeel/plaf.html 
         */
        try {
            for (javax.swing.UIManager.LookAndFeelInfo info : javax.swing.UIManager.getInstalledLookAndFeels()) {
                if ("Nimbus".equals(info.getName())) {
                    javax.swing.UIManager.setLookAndFeel(info.getClassName());
                    break;
                }
            }
        } catch (ClassNotFoundException ex) {
            java.util.logging.Logger.getLogger(Game2048.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (InstantiationException ex) {
            java.util.logging.Logger.getLogger(Game2048.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (IllegalAccessException ex) {
            java.util.logging.Logger.getLogger(Game2048.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        } catch (javax.swing.UnsupportedLookAndFeelException ex) {
            java.util.logging.Logger.getLogger(Game2048.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        }
        //</editor-fold>

        /* Create and display the form */
        java.awt.EventQueue.invokeLater(new Runnable() {
            public void run() {
                new Game2048().setVisible(true);
            }
        });
    }

    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JLabel jLabel00;
    private javax.swing.JLabel jLabel01;
    private javax.swing.JLabel jLabel02;
    private javax.swing.JLabel jLabel03;
    private javax.swing.JLabel jLabel1;
    private javax.swing.JLabel jLabel10;
    private javax.swing.JLabel jLabel11;
    private javax.swing.JLabel jLabel12;
    private javax.swing.JLabel jLabel13;
    private javax.swing.JLabel jLabel20;
    private javax.swing.JLabel jLabel21;
    private javax.swing.JLabel jLabel22;
    private javax.swing.JLabel jLabel23;
    private javax.swing.JLabel jLabel30;
    private javax.swing.JLabel jLabel31;
    private javax.swing.JLabel jLabel32;
    private javax.swing.JLabel jLabel33;
    private javax.swing.JLabel jLabelGameOver;
    private javax.swing.JLabel jLabelScore;
    private javax.swing.JLabel jLabelScoreNum;
    private javax.swing.JPanel jPanelBottom;
    private javax.swing.JPanel jPanelMiddle;
    private javax.swing.JPanel jPanelTop;
    // End of variables declaration//GEN-END:variables
}
