#!/usr/bin/env python3
"""
Laboratory Work No. 2: Cryptanalysis of Monoalphabetic Ciphers.
Student: Șoimu Ionuț (FAF-243)
Supervisor: asist. univ. Zaica Maia

CLI Tool for Monoalphabetic Cryptanalysis, Statistical Profiling,
Progressive Milestone Walkthrough, and Key Recovery.
"""

import argparse
import sys
from frequency_analysis import FrequencyAnalyzer
from cipher_solver import CipherSolver, SOLVED_KEY

# Variant 22 (V22) Ciphertext from Lab Guide
DEFAULT_VARIANT_22 = (
    "Rqxsv Qviaviw Ftiosvf ztf av wqv avpw lgnrg hifuwnsnjxpw,dghngwvpwtasf wqv jivtwvpw xp Rxssxtz Civovixhl Cixvoztg. "
    "Dgsxlv qxphngwvzunitif, qxp vzxgvghv xp odv znpw vzuqtwxhtssf wn rqtw qv oxo.Xgovvo, wrn zniv oxppxzxsti zvg xg t pxgjsv "
    "cxvso htg phtihvsf avxztjxgvo. Rqviv Ftiosvf rtp Itavstxpxtg, ndwjnxgj, pduvicxhxts, civv tgovtpf rxwq wqv ovwtxsp nc t "
    "jnno pwnif, tgo vkvi ivtof cni wqv ztxg hqtghv,Cixvoztg wvgovo wnrtio xgwinkvipxng, ovuwq nc pwdof, uvipngts pvhdixwf,"
    "wxzxoxwf, ovoxhtwxng, tgo thhdithf, gxhvwf, tgo ktsxoxwf nc rnil. Ovpuxwvwqv ivstwxkv oitagvpp nc wqvpv uvipngts witxwp—"
    "ni uviqtup avhtdpv ncwqvz, Cixvoztg'p wqvnivwxhts hngwixadwxngp tgo qxp uithwxhts twwtxgzvgwpvyhvvo wqnpv nc tgf nwqvi "
    "hifuwnsnjxpw. Ftiosvf'p htivvi rtp sxlv tgtztmxgj plfinhlvw wqtw vyusnovp xg ctgwtpwxh utwwvigp tjtxgpw wqvqvtkvgp. "
    "Cixvoztg'p rtp sxlv wqv pdg.Qv rtp anig Rnscv Cixvoztg ng Pvuwvzavi 24, 1891, xg Lxpqxgvk,Idppxt, wqv nsovpw png tgo pvhngo "
    "hqxso nc Civovixhl tgo Inpt Cixvoztg.Qxp ctwqvi, t Idztgxtg rqn punlv vxjqw stgjdtjvp tgo rnilvo tp tgxgwviuivwvi cni wqv "
    "Idppxtg Unpw Nccxhv, vzxjitwvo wn Tzvixht xg 1892, tw rqxhq wxzv qxp png'p gtzv rtp hqtgjvo wn Rxssxtz. Wqv ctzxsf pvwwsvoxg "
    "Uxwwpadijq, rqviv qxp ctwqvi ztgtjvo t pvrxgj zthqxgv tjvghf.Rxssxtz jitodtwvo xg 1909 tp ngv nc wqv wvg qngni pwdovgwp xg t "
    "hstpp nc300 tw Uxwwpadijq Hvgwits Qxjq Phqnns; qv wqvg rvgw wn rnil tp hqxvchsvil xg wqv Vixv Hxwf Xing Rnilp, t cxiz wqtw "
    "pnso pwvtz vgjxgvp. Tandwwqtw wxzv wqv athl-wn-wqv-ctiz znkvzvgw htssvo wn hxwf anfp, tgo xg wqvctss nc 1910, Cixvoztg tgo "
    "wqivv cixvgop vginssvo xg ZxhqxjtgTjixhdswdits Hnssvjv, rqnpv hqxvc twwithwxng rtp wqtw xw rtp wdxwxng-civv.Adw Cixvoztg pnng "
    "oxphnkvivo wqtw ctizxgj qvso sxwwsv xgwvivpw cni qxz.Qv rtp tg xgkvgwxkv fndgj cvssnr rqn sxlvo wn cxy wqxgjp tgo qto "
    "rixwwvgpnzv phxvghv cxhwxng cni qxp qxjq-phqnns utuvi; qv rtp ituxosf hnzxgj wnwqv hnghsdpxng wqtw qv sxlvo phxvghv. Tw wqv "
    "vgo nc wqv wviz qv svtigvowqtw wdxwxng rtp tspn civv xg t phxvgwxcxh cxvso tssxvo wn tjixhdswdiv—jvgvwxhp—tw ngv nc wqv Xkf "
    "Svtjdv dgxkvipxwxvp, Hnigvss. Qv aniinrvowitxg ctiv tgo tiixkvo xg Xwqtht, Gvr Fnil, xg Cvaidtif, 1911, rqviv qvjnw t ena "
    "rtxwxgj ng wtasvp. Tcwvi hnzzvghvzvgw xg Cvaidtif nc 1914, qvtwwvgovo jitodtwv phqnns, ztgtjxgj wn ctss xg snkv wrxhv, "
    "nghv rxwq taidgvwwv, nghv rxwq wqv asngov otdjqwvi nc t znkxv-qndpv nrgvi. Rqxsvqv rtp wqviv, t rvtswqf wvywxsv zvihqtgw, "
    "Jvnijv Ctaftg, rqnztxgwtxgvo stanitwnixvp xg thndpwxhp, hqvzxpwif, jvgvwxhp, tgo hifu-wnsnjf (wn wif wn uinkv wqtw Athng "
    "rinwv Pqtlvpuvtiv'p ustfp) ng qxp 500-thiv vpwtwv, Ixkviatgl, tw Jvgvkt, Xssxgnxp, ovhxovo wqtw qv gvvovo tjvgvwxhxpw wn "
    "xzuinkv wqv jitxgp tgo sxkvpwnhl ng qxp ctiz. Qv tuusxvo wnHnigvss cni t \"rndso-av-vi,\" gnw tg \"tp-xp-vi,\" tgo qxivo "
    "Cixvoztg, wnavjxg Edgv 1, 1915.Ctaftg rtp t ztg nc gn cnizts vodhtwxng adw nc xgwvssxjvghv tgovgvijf. Qv qto t jivtw ovpxiv "
    "wn av \"pnzvanof,\" tgo wqtw ovpxivznwxktwvo qxp pdapxoxmxgj wqv Athngxtg pwdoxvp: uinnc nc wqxpivknsdwxngtif wqvpxp rndso "
    "hnkvi xwp utwing tp rvss tp xwp thwdtsoxphnkvivip rxwq jsnif. Qv qxzpvsc ivto sxwwsv, adw qv tapniavo vgndjqcinz wqnpv "
    "tindgo qxz wn ztlv qxp wtsl ng tsznpw tgf pdaevhw pndgoxzuivppxkv—tw svtpw pduvicxhxtssf. Qv rtp tdwnhitwxh, gvkvi tssnrxgj "
    "qxppwtcc wn oxptjivv rxwq qxz, adw nwqvirxpv gnw dgusvtptgw pn sngj tpvzusnfvvp ivhnjgxmvo wqtw qv rtp anpp. T htioxgts "
    "tiwxhsv nc ctxwq rxwqqxz rtp wqtw t rvss-vyvhdwvo ptsvp htzutxjg hndso udw thinpp tsznpwtgfwqxgj."
)

# Colors for terminal output
COLOR_BOLD = "\033[1m"
COLOR_CYAN = "\033[36m"
COLOR_GREEN = "\033[32m"
COLOR_YELLOW = "\033[33m"
COLOR_PURPLE = "\033[35m"
COLOR_RESET = "\033[0m"


def print_banner():
    print(f"{COLOR_PURPLE}{COLOR_BOLD}======================================================================{COLOR_RESET}")
    print(f"{COLOR_CYAN}{COLOR_BOLD}   CS LAB 2: MONOALPHABETIC CIPHER CRYPTANALYSIS (VARIANT 22)        {COLOR_RESET}")
    print(f"   Student: Șoimu Ionuț (FAF-243) | Supervisor: asist. univ. Zaica Maia")
    print(f"{COLOR_PURPLE}{COLOR_BOLD}======================================================================{COLOR_RESET}")


def run_frequency_mode(analyzer: FrequencyAnalyzer):
    print(f"\n{COLOR_GREEN}{COLOR_BOLD}[1] STATISTICAL FREQUENCY ANALYSIS{COLOR_RESET}\n")
    print(analyzer.format_frequency_table())

    print(f"\n{COLOR_YELLOW}{COLOR_BOLD}--- Top 10 Cipher Digrams ---{COLOR_RESET}")
    digrams = analyzer.compute_digram_frequencies(10)
    dg_str = ", ".join([f"{dg} ({cnt}x, {pct:.2f}%)" for dg, cnt, pct in digrams])
    print(dg_str)

    print(f"\n{COLOR_YELLOW}{COLOR_BOLD}--- Top 8 Cipher Trigrams ---{COLOR_RESET}")
    trigrams = analyzer.compute_trigram_frequencies(8)
    tg_str = ", ".join([f"{tg} ({cnt}x, {pct:.2f}%)" for tg, cnt, pct in trigrams])
    print(tg_str)

    print(f"\n{COLOR_YELLOW}{COLOR_BOLD}--- Repeated Double Letters ---{COLOR_RESET}")
    doubles = analyzer.compute_repeated_letters()
    db_str = ", ".join([f"{db} ({cnt}x)" for db, cnt in doubles[:6]])
    print(db_str)


def run_step_by_step_mode(solver: CipherSolver):
    print(f"\n{COLOR_GREEN}{COLOR_BOLD}[2] PROGRESSIVE CRYPTANALYTIC DEDUCTION WALKTHROUGH{COLOR_RESET}")
    milestones = solver.get_milestones()

    for m in milestones:
        step = m["step"]
        print(f"\n{COLOR_CYAN}{COLOR_BOLD}--- Milestone {step}: {m['title']} ---{COLOR_RESET}")
        print(f"{COLOR_BOLD}Rationale:{COLOR_RESET} {m['rationale']}")
        recovered_letters = ", ".join([f"{k}->{v}" for k, v in m['mapping'].items()])
        print(f"{COLOR_YELLOW}Active Substitutions ({len(m['mapping'])} letters):{COLOR_RESET} {recovered_letters}")

        partial_sample = solver.apply_partial_mapping(m['mapping'])[:240]
        print(f"{COLOR_BOLD}Decrypted Excerpt:{COLOR_RESET}\n{partial_sample}...\n")


def run_solve_mode(solver: CipherSolver):
    print(f"\n{COLOR_GREEN}{COLOR_BOLD}[3] FULL KEY RECOVERY & CIPHERTEXT DECRYPTION{COLOR_RESET}\n")
    print(f"{COLOR_YELLOW}{COLOR_BOLD}Reconstructed Key Table (Cipher -> Plain):{COLOR_RESET}")
    print(solver.format_key_table())

    a, b, a_inv = solver.get_affine_parameters()
    print(f"\n{COLOR_CYAN}{COLOR_BOLD}Mathematical Underlying Structure:{COLOR_RESET}")
    print(f"Cipher conforms to an Affine Cipher over Z_26:")
    print(f"  Encryption: E(x) = ({a}*x + {b}) mod 26")
    print(f"  Decryption: D(y) = {a_inv}*(y - {b}) mod 26 = ({a_inv}*y + 1) mod 26")

    print(f"\n{COLOR_GREEN}{COLOR_BOLD}Decrypted Plaintext:{COLOR_RESET}")
    print("-" * 70)
    plain = solver.decrypt()
    print(plain)
    print("-" * 70)


def interactive_menu(solver: CipherSolver, analyzer: FrequencyAnalyzer):
    while True:
        print_banner()
        print("Select an option:")
        print("  1. Statistical Frequency Profiling (Unigrams, Digrams, Trigrams, IC)")
        print("  2. Step-by-Step Progressive Cryptanalysis Walkthrough (Milestones 1-5)")
        print("  3. Recovered Key Table & Full Decrypted Text")
        print("  4. Run Full Cryptanalysis Pipeline")
        print("  5. Exit")

        choice = input("\nEnter choice [1-5]: ").strip()
        if choice == "1":
            run_frequency_mode(analyzer)
        elif choice == "2":
            run_step_by_step_mode(solver)
        elif choice == "3":
            run_solve_mode(solver)
        elif choice == "4":
            run_frequency_mode(analyzer)
            run_step_by_step_mode(solver)
            run_solve_mode(solver)
        elif choice == "5":
            print("Exiting.")
            sys.exit(0)
        else:
            print("Invalid option. Please try again.")

        input("\nPress Enter to continue...")


def main():
    parser = argparse.ArgumentParser(
        description="Monoalphabetic Cipher Cryptanalysis & Frequency Analysis CLI"
    )
    parser.add_argument(
        "-f", "--frequency", action="store_true", help="Display frequency analysis tables and IC"
    )
    parser.add_argument(
        "-s", "--steps", action="store_true", help="Display progressive step-by-step cryptanalysis"
    )
    parser.add_argument(
        "-d", "--solve", action="store_true", help="Display reconstructed key table and full decrypted text"
    )
    parser.add_argument(
        "-a", "--all", action="store_true", help="Run full pipeline (frequency, steps, full decryption)"
    )
    parser.add_argument(
        "-i", "--interactive", action="store_true", help="Run interactive menu mode"
    )
    parser.add_argument(
        "--file", type=str, default=None, help="Path to custom ciphertext file"
    )

    args = parser.parse_args()

    # Load text
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        text = DEFAULT_VARIANT_22

    analyzer = FrequencyAnalyzer(text)
    solver = CipherSolver(text)

    # If flags passed
    if args.frequency or args.steps or args.solve or args.all:
        print_banner()
        if args.frequency or args.all:
            run_frequency_mode(analyzer)
        if args.steps or args.all:
            run_step_by_step_mode(solver)
        if args.solve or args.all:
            run_solve_mode(solver)
    else:
        # Default or interactive
        interactive_menu(solver, analyzer)


if __name__ == "__main__":
    main()
