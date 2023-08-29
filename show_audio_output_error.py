import json
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy


def main():
    with open("raw-data/v2/north.json") as f:
        d = json.load(f)

        fig, axs = plt.subplots(1, 5)

        x = []
        y1 = []
        y2 = []
        y3 = []
        y4 = []
        y5 = []
        c = []

        synth_data = [
            [0.0, 0.0, 0.0, 0.0],
            [
                10.006712282059766,
                -10.006712282059766,
                -11.505482840300715,
                11.505482840300715,
            ],
            [
                18.556881063290305,
                -18.556881063290305,
                -24.467509181430664,
                24.467509181430664,
            ],
            [
                25.76611398952776,
                -25.76611398952776,
                -38.77047137755371,
                38.77047137755371,
            ],
            [
                31.796318351337135,
                -31.796318351337135,
                -54.252462138104804,
                54.252462138104804,
            ],
            [
                36.825584940357984,
                -36.825584940357984,
                -70.73539067144443,
                70.73539067144443,
            ],
            [
                41.02516958487952,
                -41.02516958487952,
                -88.04800114928337,
                88.04800114928337,
            ],
        ]

        for i in range(84):
            block = int(i) // 12
            hit_weight = (int(i) % 12) // 4

            ptp1 = numpy.ptp(d["non_filtered"]["256_nonparabolic"][f"{i}"])
            ptp2 = numpy.ptp(d["non_filtered"]["512_nonparabolic"][f"{i}"])
            ptp3 = numpy.ptp(d["120hp"]["512_nonparabolic"][f"{i}"])
            ptp4 = numpy.ptp(d["500hp"]["512_nonparabolic"][f"{i}"])
            ptp5 = numpy.ptp(synth_data[block])

            print(f"{i} - {ptp1} - hit weight: {hit_weight}")
            if (int(i) % 12) == 11:
                print(" -- ")

            x.append(block)
            y1.append(ptp1)
            y2.append(ptp2)
            y3.append(ptp3)
            y4.append(ptp4)
            y5.append(ptp5)
            c.append(hit_weight)

        print(c)
        axs[0].set_title("non filtered 256 non parabolic")
        axs[0].scatter(x, y1, c=c)
        axs[1].set_title("non filtered 512 non parabolic")
        axs[1].scatter(x, y2, c=c)
        axs[2].set_title("120hp 512 non parabolic")
        axs[2].scatter(x, y3, c=c)
        axs[3].set_title("500hp 512 non parabolic")
        axs[3].scatter(x, y4, c=c)
        axs[4].set_title("synthetic")
        axs[4].scatter(x, y5, c=c)

        # all_limits = [axs[0].get_ylim(), axs[1].get_ylim(), axs[2].get_ylim(), axs[3].get_ylim()]
        # print(all_limits)
        # print(max(all_limits))
        # max_lim = max(all_limits)

        # I happen to know this has the biggest limit
        max_lim = axs[3].get_ylim()

        axs[0].set_ylim(max_lim)
        axs[1].set_ylim(max_lim)
        axs[2].set_ylim(max_lim)
        axs[3].set_ylim(max_lim)
        axs[4].set_ylim(max_lim)
        plt.show()


if __name__ == "__main__":
    main()
